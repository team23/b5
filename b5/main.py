import argparse
import os
import subprocess
import sys

import termcolor

from .exceptions import B5ExecutionError
from .lib.config import load_config
from .lib.detect import detect_project_path, DETECT
from .lib.taskfile import find_taskfiles
from .lib.config import find_configs
from .lib.script import StoredScriptSource, construct_script_source, construct_script_run
from .lib.state import State
from . import VERSION


def main():
    try:
        # Parse all arguments
        parser = argparse.ArgumentParser(
            prog='b5',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            '-p', '--project-path', nargs='?',
            help='Project path if not part of parent paths, normally b5 tries to get the project path by itself',
            dest='project_path',
        )
        parser.add_argument(
            '-r', '--run-path', nargs='?',
            help='Path inside the project b5 will execute in (cd into)',
            dest='run_path', default='build',
        )
        parser.add_argument(
            '-d', '--detect', nargs='?',
            help='Project detection',
            default='git', choices=DETECT,
            dest='detect',
        )
        parser.add_argument(
            '-c', '--config', nargs='?', action='append',
            help='Path to config (inside run path)',
            dest='configfiles',
        )
        parser.add_argument(
            '-t', '--taskfile', nargs='?', action='append',
            help='Path to Taskfile (inside run path)',
            dest='taskfiles',
        )
        parser.add_argument(
            '-s', '--shell', nargs='?',
            help='Shell to run the generated script in (should be bash)',
            dest='shell',
            default='/bin/bash',
        )
        parser.add_argument('command')
        parser.add_argument('command_args', nargs=argparse.REMAINDER)
        sys_args = sys.argv[1:]
        if not sys_args:
            sys_args = ['help']
        args = parser.parse_args(args=sys_args)
        if args.taskfiles is None:
            args.taskfiles = ['~/.b5/Taskfile', 'Taskfile', 'Taskfile.local']
        if args.configfiles is None:
            args.configfiles = ['~/.b5/config.yml', 'config.yml', 'config.local.yml', 'local.yml']

        # State vars
        state = State(
            project_path = args.project_path,
            run_path = None,
            taskfiles = [],
            config = {},
            args = vars(args)
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

        # Run header
        print('b5 %s' % VERSION)
        if state.project_path is not None:
            print('Found project path (%s)' % state.project_path)
            if state.taskfiles:
                print('Found Taskfile (%s)' % ', '.join([t['taskfile'] for t in state.taskfiles]))
        print('Executing task %s' % args.command)
        print('')  # empty line

        with state.stored() as _stored_state:
            # Construct and execute bash script (and Taskfile)
            script_source = '\n'.join([
                construct_script_source(state),
                construct_script_run(state),
            ])
            with StoredScriptSource(state, script_source) as source:
                # print(source.source)
                # return
                if state.run_path:
                    os.chdir(state.run_path)
                try:
                    result = subprocess.run(
                        [
                            args.shell,
                            source.name,
                        ],
                        shell=False,
                        check=True,
                    )
                except KeyboardInterrupt:
                    sys.exit(0)
                except subprocess.CalledProcessError:
                    termcolor.cprint('Task execution failed, see above', color='red')
                    sys.exit(1)
                #print(result)
    except B5ExecutionError as e:
        termcolor.cprint(str(e), 'red')
        sys.exit(1)
