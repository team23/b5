import os


def detect_git(path: str) -> bool:
    git_path = os.path.join(path, '.git')
    # `.git` is a directory in a normal checkout, but only a file (containing a
    # `gitdir:` pointer) inside linked worktrees and submodules - accept both.
    return os.path.exists(git_path)


def detect_hg(path: str) -> bool:
    git_path = os.path.join(path, '.hg')
    return os.path.exists(git_path) and os.path.isdir(git_path)


DETECT = {
    'git': detect_git,
    'hg': detect_hg,
}


def detect_project_path(path: str, detect: str) -> str:
    path = os.path.realpath(path)
    while not DETECT[detect](path):
        parent_path = os.path.dirname(path)
        if parent_path == path:
            return None
        path = parent_path
    return path
