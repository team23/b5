import os
import subprocess
import sys

import termcolor

from b5.lib.argumentparser import MainArgumentParser
from b5 import VERSION
from b5.exceptions import B5ExecutionError
from b5.lib.config import find_configs
from b5.lib.config import load_config
from b5.lib.detect import detect_project_path
from b5.lib.script import StoredScriptSource, construct_script_source, construct_script_run
from b5.lib.state import State
from b5.lib.taskfile import find_taskfiles


def main():
    try:
        # Parse all arguments
        parser = MainArgumentParser('b5')
        parser.add_arguments()
        parser.set_default('taskfiles', ['~/.b5/Taskfile', 'Taskfile', 'Taskfile.local'])
        parser.set_default('configfiles', ['~/.b5/config.yml', 'config.yml', 'config.local.yml', 'local.yml'])
        args = parser.parse(sys.argv[1:], True)

        # State vars
        state = State(
            project_path=args.project_path,
            run_path=None,
            taskfiles=[],
            config={},
            args=vars(args)
        )

        # Find project dir
        if state.project_path is None:
            state.project_path = detect_project_path(os.getcwd(), args.detect)
        if state.project_path is not None:
            state.run_path = os.path.join(state.project_path, args.run_path)
            if not os.path.exists(state.run_path) or not os.path.isdir(state.run_path):
                raise B5ExecutionError('Run path does not exist (%s)' % state.run_path)
            state.taskfiles = find_taskfiles(state, args.taskfiles)
            state.configfiles = find_configs(state, args.configfiles)
            state.config = load_config(state)

        def _print(*args, **kwargs):
            if state.args['quiet']:
                return
            termcolor.cprint(*args, **kwargs)

        # Run header
        _print('b5 %s' % VERSION)
        if state.project_path is not None:
            _print('Found project path (%s)' % state.project_path)
            if state.taskfiles:
                _print('Found Taskfile (%s)' % ', '.join([t['taskfile'] for t in state.taskfiles]))
        _print('Executing task %s' % args.command)
        _print('')  # empty line

        with state.stored() as _stored_state:
            # Construct and execute bash script (and Taskfile)
            script_source = '\n'.join([
                construct_script_source(state),
                construct_script_run(state),
            ])
            with StoredScriptSource(state, script_source) as source:
                if state.run_path:
                    os.chdir(state.run_path)
                proc = subprocess.Popen(
                    [
                        args.shell,
                        source.name,
                    ],
                    shell=False,
                )
                try:
                    proc.wait()
                except KeyboardInterrupt:
                    termcolor.cprint('Received keyboard interrupt, waiting for task to exit...', color='yellow', end='', flush=True)
                    try:
                        proc.wait(timeout=30)
                    except subprocess.TimeoutExpired:
                        termcolor.cprint('still waiting, sending SIGTERM...', color='yellow', end='', flush=True)
                        proc.terminate()
                        try:
                            proc.wait(timeout=30)
                        except subprocess.TimeoutExpired:
                            termcolor.cprint('did not exit, sending SIGKILL', color='red')
                            proc.kill()
                            sys.exit(1)
                    termcolor.cprint('exited ok', color='yellow')
                    sys.exit(0)
                if proc.returncode == 0:
                    _print('Task exited ok', color='green')
                else:
                    termcolor.cprint('Task execution failed, see above', color='red')
                    sys.exit(1)
    except B5ExecutionError as error:
        termcolor.cprint(str(error), 'red')
        sys.exit(1)

if __name__ == '__main__':
    main()
