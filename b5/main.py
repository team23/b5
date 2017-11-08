import argparse
import os
import shlex
import subprocess

from . import VERSION
from .lib.detect import DETECT


def detect_project_path(path, detect):
    path = os.path.realpath(path)
    while not DETECT[detect](path):
        parent_path = os.path.dirname(path)
        if parent_path == path:
            return None
        path = parent_path
    return path


def find_taskfiles(project_path, taskfiles, ignore_missing=False):
    project_path = os.path.realpath(project_path)
    found_taskfiles = []
    for taskfile in taskfiles:
        taskfile_path = os.path.join(project_path, os.path.expanduser(taskfile))
        if os.path.exists(taskfile_path):
            found_taskfiles.append((taskfile, taskfile_path))
        elif not ignore_missing:
            raise RuntimeError('Taskfile %s not found' % taskfile)
    if not found_taskfiles:
        raise RuntimeError('No Taskfiles found')
    return found_taskfiles


def construct_script_source(project_path, run_path, taskfiles, command, args):
    from . import B5_BASH_PATH

    script = ''
    script += open(os.path.join(B5_BASH_PATH, 'init.sh'), 'r').read()
    script += open(os.path.join(B5_BASH_PATH, 'functions.sh'), 'r').read()
    script += open(os.path.join(B5_BASH_PATH, 'default_tasks.sh'), 'r').read()

    script += 'PROJECT_PATH=%s\n' % shlex.quote(project_path)
    script += 'RUN_PATH=%s\n' % shlex.quote(run_path)
    script += 'TASKFILE_PATHS=(%s)\n' % ' '.join([shlex.quote(t[1]) for t in taskfiles])

    script += 'BUILD_PATH=%s\n' % shlex.quote(run_path)  # backwards compatibility
    script += 'TASKFILE_PATH=%s\n' % shlex.quote(taskfiles[0][1])  # backwards compatibility

    script += 'cd %s\n' % shlex.quote(run_path)
    for taskfile in taskfiles:
        script += 'source %s\n' % shlex.quote(taskfile[1])

    script += 'b5:function_exists %s && b5:run %s || b5:error "Task not found" \n' % (
        shlex.quote('task:%s' % command),
        ' '.join(
            [shlex.quote('task:%s' % command)] + [shlex.quote(a) for a in args]
        )
    )

    return script


def main():
    # Parse all arguments
    parser = argparse.ArgumentParser(prog='b5', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-p', '--project', nargs='?',
        help='Project path if not part of parent paths, normally b5 tried to get the project path by itself',
        dest='project',
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
    project_path = args.project
    run_path = None
    taskfiles = []

    # Find project dir
    if project_path is None:
        project_path = detect_project_path(os.getcwd(), args.detect)
    if project_path is not None:
        run_path = os.path.join(project_path, args.run_path)
        taskfiles = find_taskfiles(project_path, args.taskfiles, args.ignore_missing)

    # Run header
    print('b5 %s' % VERSION)
    if project_path is not None:
        print('Found project path (%s)' % project_path)
        if taskfiles:
            print('Found Taskfile (%s)' % ', '.join([t[0] for t in taskfiles]))
    print('Executing task %s' % args.command)
    print('')  # empty line

    script = construct_script_source(project_path, run_path, taskfiles, args.command, args.args)
    #print(script)
    result = subprocess.run(
        args.shell,
        input=script.encode('utf-8'),
        #stdout=subprocess.PIPE,
        #stderr=subprocess.PIPE,
        shell=False,
        check=True,
    )
    #print(result)




