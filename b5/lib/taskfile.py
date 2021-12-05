import os
from typing import Dict, List

from ..exceptions import B5ExecutionError
from .state import State


def find_taskfiles(state: State, taskfiles: List[str]) -> List[Dict[str, str]]:
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
        raise B5ExecutionError('No Taskfiles found, tried %s inside %s' % (', '.join(taskfiles), run_path))
    return found_taskfiles
