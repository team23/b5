import os
import re
import shlex
import tempfile
from types import TracebackType
from typing import Any, Dict, Optional, Type

from .module import load_module
from .state import State

RE_KEY_ESCAPE = re.compile('[^a-zA-Z0-9]+')
CONFIG_SUB = '%s_%s'
CONFIG_KEYS = '%s_KEYS'


def modules_script_source(state: State) -> str:
    script = []
    if 'modules' in state.config:
        for module_key in state.config['modules']:
            module = load_module(state, module_key)
            script.append(module.get_script())
    return '\n'.join(script)


def config_script_source(config: Dict[str, Any], prefix: str = 'CONFIG') -> str:
    def _gen_config(config_node: Any, prefix: str) -> str:
        script = []

        if isinstance(config_node, dict):
            for key in config_node:
                escaped_key = RE_KEY_ESCAPE.sub('_', key)
                script.append(_gen_config(config_node[key], CONFIG_SUB % (prefix, escaped_key)))
            script.append('%s=(%s)' % (CONFIG_KEYS % prefix, ' '.join([shlex.quote(k) for k in config_node])))
        elif isinstance(config_node, list):
            script.append('%s=(%s)' % (prefix, ' '.join([
                shlex.quote(k)
                for k
                in config_node
                # Make sure we can escape this bit - if not just skip it
                if isinstance(k, (str, bytes))
            ])))
        elif isinstance(config_node, (str, bytes)):
            script.append('%s=%s' % (prefix, shlex.quote(config_node)))
        elif isinstance(config_node, (bool)):
            script.append('%s=%s' % (prefix, '1' if config_node else '0'))
        elif isinstance(config_node, (int, float)):
            script.append('%s=%s' % (prefix, shlex.quote(str(config_node))))
        elif config_node is None:
            script.append('%s=""' % prefix)
        else:
            raise RuntimeError('Unknown type for config export %s' % type(config_node))

        return '\n'.join(script)

    return _gen_config(config, prefix)


def construct_script_source(state: State) -> str:
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
        # Provide state for subshells and called programs (B5 prefix added)
        script.append('export B5_STATE_FILE="${STATE_FILE}"')

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
        script.append(open(taskfile['path'], 'r').read())

    return '\n'.join(script)


def construct_script_run(state: State) -> str:
    # Run everything
    return '''
TASKNAME={taskname}
_DEBUG_TRACEBACK={traceback}
if b5:function_exists {taskfunc}
then
    b5:run {taskfunc} {taskparams}
else
    b5:abort "Task $TASKNAME not found, see 'b5 help'"
fi
    '''.format(
        taskname=shlex.quote(state.args['command']),
        taskfunc=shlex.quote('task:%s' % state.args['command']),
        taskparams=' '.join(
            [shlex.quote(a) for a in state.args['command_args']],
        ),
        traceback='1' if state.args['traceback'] else '0',
    )


class StoredScriptSource:
    def __init__(self, state: State, source: str) -> None:
        self.state = state
        self.source = source
        self.file_handle = tempfile.NamedTemporaryFile(suffix='b5-compiled', delete=False)
        self.file_handle.write(self.source.encode('utf-8'))
        self.file_handle.close()

    def close(self) -> None:
        os.unlink(self.file_handle.name)

    def __enter__(self) -> "StoredScriptSource":
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc: Optional[BaseException],
            traceback: Optional[TracebackType],
    ) -> None:
        self.close()

    @property
    def name(self) -> str:
        return self.file_handle.name
