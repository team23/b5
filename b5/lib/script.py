import shlex
import tempfile
import os

from .module import load_module


def modules_script_source(state):
    script = []
    if 'modules' in state.config:
        for module_key in state.config['modules']:
            module = load_module(state, module_key)
            script.append(module.get_script())
    return '\n'.join(script)


def config_script_source(config, prefix='CONFIG'):
    CONFIG_SUB = '%s_%s'
    CONFIG_KEYS = '%s_KEYS'

    def _gen_config(config_node, prefix):
        script = []

        if isinstance(config_node, dict):
            for key in config_node:
                script.append(_gen_config(config_node[key], CONFIG_SUB % (prefix, key)))
            script.append('%s=(%s)' % (CONFIG_KEYS % prefix, ' '.join([shlex.quote(k) for k in config_node])))
        elif isinstance(config_node, list):
            script.append('%s=(%s)' % (prefix, ' '.join([shlex.quote(k) for k in config_node])))
        elif isinstance(config_node, (str, bytes)):
            script.append('%s=%s' % (prefix, shlex.quote(config_node)))
        elif isinstance(config_node, (int, float)):
            script.append('%s=%s' % (prefix, shlex.quote(str(config_node))))
        elif config_node is None:
            script.append('%s=""' % prefix)
        else:
            raise RuntimeError('Unknown type for config export %s' % type(config_node))

        return '\n'.join(script)

    return _gen_config(config, prefix)


def construct_script_source(state):
    from .. import B5_BASH_PATH

    script = []

    # Basic script initialisation
    script.append(open(os.path.join(B5_BASH_PATH, 'init.sh'), 'r').read())
    script.append(open(os.path.join(B5_BASH_PATH, 'functions.sh'), 'r').read())
    script.append(open(os.path.join(B5_BASH_PATH, 'default_tasks.sh'), 'r').read())

    # State
    script.append('PROJECT_PATH=%s\n' % shlex.quote(state.project_path))
    script.append('RUN_PATH=%s\n' % shlex.quote(state.run_path))
    script.append('TASKFILE_PATHS=(%s)\n' % ' '.join([shlex.quote(t['path']) for t in state.taskfiles]))
    script.append('CONFIG_PATHS=(%s)\n' % ' '.join([shlex.quote(c['path']) for c in state.configfiles]))
    if state.stored_name:
        script.append('STATE_FILE=%s\n' % shlex.quote(state.stored_name))

    # BACKWARDS COMPATIBILITY AND LEGACY CODE
    script.append('BUILD_PATH=%s\n' % shlex.quote(state.run_path))  # backwards compatibility
    if state.taskfiles:
        script.append('TASKFILE_PATH=%s\n' % shlex.quote(state.taskfiles[0]['path']))  # backwards compatibility

    # Generated sources
    script.append(config_script_source(state.config))
    script.append(modules_script_source(state))

    # run_path and parse Taskfile's
    script.append('cd %s\n' % shlex.quote(state.run_path))
    for taskfile in state.taskfiles:
        script.append('source %s\n' % shlex.quote(taskfile['path']))

    return '\n'.join(script)


def construct_script_run(state):
    # Run everything
    return 'b5:function_exists %s && b5:run %s || b5:error "Task not found" \n' % (
        shlex.quote('task:%s' % state.args['command']),
        ' '.join(
            [shlex.quote('task:%s' % state.args['command'])] + [shlex.quote(a) for a in state.args['command_args']]
        )
    )


class StoredScriptSource(object):
    def __init__(self, state, source):
        self.state = state
        self.source = source
        self.fh = tempfile.NamedTemporaryFile(suffix='b5-compiled', delete=False)
        self.fh.write(self.source.encode('utf-8'))
        self.fh.close()

    def close(self):
        os.unlink(self.fh.name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def name(self):
        return self.fh.name
