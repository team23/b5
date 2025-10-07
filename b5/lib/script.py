import os
import re
import shlex
import tempfile
from types import TracebackType
from typing import Any

from .module import load_module
from .state import State

RE_KEY_ESCAPE = re.compile('[^a-zA-Z0-9]+')
CONFIG_SUB = '{prefix}_{key}'
CONFIG_KEYS = '{key}_KEYS'


def modules_script_source(state: State) -> str:
    script = []
    if 'modules' in state.config:
        for module_key in state.config['modules']:
            module = load_module(state, module_key)
            script.append(module.get_script())
    return '\n'.join(script)


def config_script_source(config: dict[str, Any], prefix: str = 'CONFIG') -> str:
    def _gen_config(config_node: Any, prefix: str) -> str:
        script = []

        if isinstance(config_node, dict):
            for key in config_node:
                escaped_key = RE_KEY_ESCAPE.sub('_', key)
                script.append(_gen_config(config_node[key], CONFIG_SUB.format(prefix=prefix,key=escaped_key)))
            script.append(f"{CONFIG_KEYS.format(key=prefix)}=({' '.join([shlex.quote(k) for k in config_node])})")
        elif isinstance(config_node, list):
            list_contents = ' '.join([
                shlex.quote(k)
                for k
                in config_node
                # Make sure we can escape this bit - if not just skip it
                if isinstance(k, str | bytes)
            ])
            script.append(f'{prefix}=({list_contents})')
        elif isinstance(config_node, str | bytes):
            script.append(f'{prefix}={shlex.quote(config_node)}')
        elif isinstance(config_node, bool):
            script.append(f"{prefix}={'1' if config_node else '0'}")
        elif isinstance(config_node, int | float):
            script.append(f'{prefix}={shlex.quote(str(config_node))}')
        elif config_node is None:
            script.append(f'{prefix}=""')
        else:
            raise RuntimeError(f'Unknown type for config export {type(config_node)}')

        return '\n'.join(script)

    return _gen_config(config, prefix)


def construct_script_source(state: State) -> str:
    from .. import B5_BASH_PATH

    script = []

    # Basic script initialisation
    script.append(open(os.path.join(B5_BASH_PATH, 'init.sh')).read())
    script.append(open(os.path.join(B5_BASH_PATH, 'functions.sh')).read())
    script.append(open(os.path.join(B5_BASH_PATH, 'default_tasks.sh')).read())

    # State
    script.append(f'PROJECT_PATH={shlex.quote(state.project_path)}\n')
    script.append(f'RUN_PATH={shlex.quote(state.run_path)}\n')
    script.append(f"TASKFILE_PATHS=({' '.join([shlex.quote(t['path']) for t in state.taskfiles])})\n")
    script.append(f"CONFIG_PATHS=({' '.join([shlex.quote(c['path']) for c in state.configfiles])})\n")
    if state.stored_name:
        script.append(f'STATE_FILE={shlex.quote(state.stored_name)}\n')
        # Provide state for subshells and called programs (B5 prefix added)
        script.append('export B5_STATE_FILE="${STATE_FILE}"')

    # BACKWARDS COMPATIBILITY AND LEGACY CODE
    script.append(f'BUILD_PATH={shlex.quote(state.run_path)}\n')  # backwards compatibility
    if state.taskfiles:
        script.append(f"TASKFILE_PATH={shlex.quote(state.taskfiles[0]['path'])}\n")  # backwards compatibility

    # Generated sources
    script.append(config_script_source(state.config))
    script.append(modules_script_source(state))

    # run_path and parse Taskfile's
    script.append(f'cd {shlex.quote(state.run_path)}\n')
    for taskfile in state.taskfiles:
        script.append(open(taskfile['path']).read())

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
        taskfunc=shlex.quote(f"task:{state.args['command']}"),
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
            exc_type: type[BaseException] | None,
            exc: BaseException | None,
            traceback: TracebackType | None,
    ) -> None:
        self.close()

    @property
    def name(self) -> str:
        return self.file_handle.name
