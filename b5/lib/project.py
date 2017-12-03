import os

from .detect import DETECT


def detect_project_path(path, detect):
    path = os.path.realpath(path)
    while not DETECT[detect](path):
        parent_path = os.path.dirname(path)
        if parent_path == path:
            return None
        path = parent_path
    return path


def find_taskfiles(state, taskfiles, ignore_missing=False):
    run_path = os.path.realpath(state.run_path)
    found_taskfiles = []
    for taskfile in taskfiles:
        taskfile_path = os.path.join(run_path, os.path.expanduser(taskfile))
        if os.path.exists(taskfile_path):
            found_taskfiles.append((taskfile, taskfile_path))
        elif not ignore_missing:
            raise RuntimeError('Taskfile %s not found' % taskfile)
    if not found_taskfiles:
        raise RuntimeError('No Taskfiles found')
    return found_taskfiles
