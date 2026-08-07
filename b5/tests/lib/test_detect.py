import os
import tempfile
import unittest

from b5.lib.detect import detect_git, detect_project_path


class TestDetectGit(unittest.TestCase):

    def test_detects_normal_checkout(self):
        with tempfile.TemporaryDirectory() as path:
            os.mkdir(os.path.join(path, '.git'))

            self.assertTrue(detect_git(path))

    def test_detects_worktree(self):
        # Inside a linked worktree (and submodules) `.git` is a file containing
        # a `gitdir:` pointer instead of a directory.
        with tempfile.TemporaryDirectory() as path:
            with open(os.path.join(path, '.git'), 'w') as git_file:
                git_file.write('gitdir: /somewhere/.git/worktrees/example\n')

            self.assertTrue(detect_git(path))

    def test_no_git(self):
        with tempfile.TemporaryDirectory() as path:
            self.assertFalse(detect_git(path))

    def test_detect_project_path_in_worktree(self):
        with tempfile.TemporaryDirectory() as path:
            project_path = os.path.realpath(path)
            with open(os.path.join(project_path, '.git'), 'w') as git_file:
                git_file.write('gitdir: /somewhere/.git/worktrees/example\n')
            sub_path = os.path.join(project_path, 'build')
            os.mkdir(sub_path)

            self.assertEqual(project_path, detect_project_path(sub_path, 'git'))
