import os
import shlex

from .module import module_load


def _modules_script_source(project_path, run_path, config):
    script = []
    if 'modules' in config:
        for module_key in config['modules']:
            module_config = config['modules'][module_key]
            module = module_load(project_path, run_path, module_key, module_config, config)
            script.append(module.get_script())
    return '\n'.join(script)


def _config_script_source(config):
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

    return _gen_config(config, 'CONFIG')


def construct_script_source(project_path, run_path, config, taskfiles, command, args):
    from .. import B5_BASH_PATH

    script = []
    script.append(open(os.path.join(B5_BASH_PATH, 'init.sh'), 'r').read())
    script.append(open(os.path.join(B5_BASH_PATH, 'functions.sh'), 'r').read())
    script.append(open(os.path.join(B5_BASH_PATH, 'legacy.sh'), 'r').read())
    script.append(open(os.path.join(B5_BASH_PATH, 'default_tasks.sh'), 'r').read())

    script.append('PROJECT_PATH=%s\n' % shlex.quote(project_path))
    script.append('RUN_PATH=%s\n' % shlex.quote(run_path))
    script.append('TASKFILE_PATHS=(%s)\n' % ' '.join([shlex.quote(t[1]) for t in taskfiles]))

    # BACKWARDS COMPATIBILITY AND LEGACY CODE
    script.append('BUILD_PATH=%s\n' % shlex.quote(run_path))  # backwards compatibility
    if taskfiles:
        script.append('TASKFILE_PATH=%s\n' % shlex.quote(taskfiles[0][1]))  # backwards compatibility
    script.append('LEGACY_MODULES_PATH=%s\n' % shlex.quote(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'legacy', 'modules')))  # legacy

    script.append(_modules_script_source(project_path, run_path, config))
    script.append(_config_script_source(config))

    script.append('cd %s\n' % shlex.quote(run_path))
    for taskfile in taskfiles:
        script.append('source %s\n' % shlex.quote(taskfile[1]))

    script.append('b5:function_exists %s && b5:run %s || b5:error "Task not found" \n' % (
        shlex.quote('task:%s' % command),
        ' '.join(
            [shlex.quote('task:%s' % command)] + [shlex.quote(a) for a in args]
        )
    ))

    return '\n'.join(script)
