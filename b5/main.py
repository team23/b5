import argparse
import os
import subprocess

from .lib.config import load_config
from .lib.project import detect_project_path, find_taskfiles
from .lib.script import construct_script_source
from .lib.detect import DETECT
from . import VERSION


def main():
    # Parse all arguments
    parser = argparse.ArgumentParser(prog='b5', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
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
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.taskfiles is None:
        args.taskfiles = ['~/.b5/Taskfile', 'build/Taskfile', 'build/Taskfile.local']
        args.ignore_missing = True

    # State vars
    project_path = args.project_path
    run_path = None
    taskfiles = []
    config = {}

    # Find project dir
    if project_path is None:
        project_path = detect_project_path(os.getcwd(), args.detect)
    if project_path is not None:
        run_path = os.path.join(project_path, args.run_path)
        if not os.path.exists(run_path) or not os.path.isdir(run_path):
            raise RuntimeError('Run path does not exist')
        taskfiles = find_taskfiles(project_path, args.taskfiles, args.ignore_missing)
        config = load_config(run_path)

    # Run header
    print('b5 %s' % VERSION)
    if project_path is not None:
        print('Found project path (%s)' % project_path)
        if taskfiles:
            print('Found Taskfile (%s)' % ', '.join([t[0] for t in taskfiles]))
    print('Executing task %s' % args.command)
    print('')  # empty line

    script = construct_script_source(project_path, run_path, config, taskfiles, args.command, args.args)
    print(script)
    result = subprocess.run(
        args.shell,
        input=script.encode('utf-8'),
        #stdout=subprocess.PIPE,
        #stderr=subprocess.PIPE,
        shell=False,
        check=True,
    )
    #print(result)
