import argparse
import os
import subprocess
import sys

from .lib.config import load_config
from .lib.project import detect_project_path, find_taskfiles
from .lib.script import StoredScriptSource
from .lib.detect import DETECT
from .lib.state import State
from . import VERSION


def main():
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
    # TODO: Add config params (config.yml/local.yml)
    parser.add_argument(
        '-d', '--detect', nargs='?',
        help='Project detection',
        default='git', choices=DETECT,
        dest='detect',
    )
    parser.add_argument(
        '-t', '--taskfile', nargs='?', action='append',
        help='Path to Taskfile inside project',
        dest='taskfiles',
    )
    parser.add_argument(
        '-m', '--ignore-missing', nargs='?',
        help='Ignore missing Taskfile, probably only necessary if you use multiple -t/--taskfile',
        dest='ignore_missing',
        default=False,
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
        args.ignore_missing = True

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
            raise RuntimeError('Run path does not exist')
        state.taskfiles = find_taskfiles(state, args.taskfiles, args.ignore_missing)
        state.config = load_config(state)

    # Run header
    print('b5 %s' % VERSION)
    if state.project_path is not None:
        print('Found project path (%s)' % state.project_path)
        if state.taskfiles:
            print('Found Taskfile (%s)' % ', '.join([t[0] for t in state.taskfiles]))
    print('Executing task %s' % args.command)
    print('')  # empty line

    with state.stored() as _stored_state:
        # Construct and execute bash script (and Taskfile)
        with StoredScriptSource(state) as source:
            # print(source.source)
            # return
            if state.run_path:
                os.chdir(state.run_path)
            result = subprocess.run(
                [
                    args.shell,
                    source.name,
                ],
                shell=False,
                check=True,
            )
            #print(result)
