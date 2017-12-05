import os


def find_taskfiles(state, taskfiles):
    run_path = os.path.realpath(state.run_path)
    found_taskfiles = []
    for taskfile in taskfiles:
        taskfile_path = os.path.join(run_path, os.path.expanduser(taskfile))
        if os.path.exists(taskfile_path):
            found_taskfiles.append({
                'taskfile': taskfile,
                'path': taskfile_path,
            })
    if not found_taskfiles:
        raise RuntimeError('No Taskfiles found')
    return found_taskfiles

