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
