import unittest

from b5.lib.argumentparser import ExecuteArgumentParser, InitArgumentParser, MainArgumentParser, TemplateArgumentParser


class TestMainArgumentParser(unittest.TestCase):

    def setUp(self):
        self.parser = MainArgumentParser()
        self.parser.add_arguments()

    def test_config_file_can_be_set(self):
        arguments = self.parser.parse(['--config', 'test.yml', 'test'])

        self.assertIn('test.yml', arguments.configfiles)

    def test_default_configfiles_will_be_set(self):
        self.parser.set_default('configfiles', ['~/.b5/config.yml', 'config.yml', 'config.local.yml', 'local.yml'])
        arguments = self.parser.parse(['test'])

        self.assertIn('~/.b5/config.yml', arguments.configfiles)
        self.assertIn('config.yml', arguments.configfiles)
        self.assertIn('config.local.yml', arguments.configfiles)
        self.assertIn('local.yml', arguments.configfiles)

    def test_taskfile_can_be_set(self):
        arguments = self.parser.parse(['--taskfile', 'DifferentTaskFile', 'test'])

        self.assertIn('DifferentTaskFile', arguments.taskfiles)

    def test_default_taskfiles_will_be_set(self):
        self.parser.set_default('taskfiles', ['~/.b5/Taskfile', 'Taskfile', 'Taskfile.local'])
        arguments = self.parser.parse(['test'])

        self.assertIn('~/.b5/Taskfile', arguments.taskfiles)
        self.assertIn('Taskfile', arguments.taskfiles)
        self.assertIn('Taskfile.local', arguments.taskfiles)

    def test_default_run_path_is_set(self):
        arguments = self.parser.parse(['test'])

        self.assertEqual('build', arguments.run_path)

    def test_run_path_can_be_set(self):
        arguments = self.parser.parse(['--run-path', 'not_the_build_folder', 'test'])

        self.assertEqual('not_the_build_folder', arguments.run_path)

    def test_default_shell_is_set(self):
        arguments = self.parser.parse(['test'])

        self.assertEqual('/bin/bash', arguments.shell)

    def test_shell_can_be_set(self):
        arguments = self.parser.parse(['--shell', '/bin/sh', 'test'])

        self.assertEqual('/bin/sh', arguments.shell)

    def test_detect_default_is_set_to_git(self):
        arguments = self.parser.parse(['test'])

        self.assertEqual('git', arguments.detect)

    def test_detect_can_be_set_to_mercurial(self):
        arguments = self.parser.parse(['--detect', 'hg', 'test'])

        self.assertEqual('hg', arguments.detect)

    def test_quiet_is_false_by_default(self):
        arguments = self.parser.parse(['test'])

        self.assertFalse(arguments.quiet)

    def test_quiet_can_be_set_to_true(self):
        arguments = self.parser.parse(['--quiet', 'true', 'test'])

        self.assertTrue(arguments.quiet)


class TestInitArgumentParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = InitArgumentParser()
        self.parser.add_arguments()

    def test_skeleton_can_be_set(self):
        arguments = self.parser.parse(['--skeleton', 'test', 'path'])

        self.assertEqual('test', arguments.skeleton)

    def test_skeleton_can_be_set_with_shortcut(self):
        arguments = self.parser.parse(['-s', 'test', 'path'])

        self.assertEqual('test', arguments.skeleton)

    def test_skeleton_has_basic_as_default(self):
        arguments = self.parser.parse(['path'])

        self.assertEqual('basic', arguments.skeleton)

    def test_branch_can_be_set(self):
        arguments = self.parser.parse(['--branch', 'test', 'path'])

        self.assertEqual('test', arguments.branch)

    def test_branch_can_be_set_with_shortcut(self):
        arguments = self.parser.parse(['-b', 'test', 'path'])

        self.assertEqual('test', arguments.branch)


class TestExecuteArgumentParser(unittest.TestCase):
    def setUp(self):
        self.parser = ExecuteArgumentParser()
        self.parser.add_arguments()

    def test_state_file_can_be_set(self):
        arguments = self.parser.parse(['--state-file', 'test'])

        self.assertEqual('test', arguments.state_file)

    def test_module_can_be_set(self):
        arguments = self.parser.parse(['--module', 'test'])

        self.assertEqual('test', arguments.module)

    def test_method_can_be_set(self):
        arguments = self.parser.parse(['--method', 'test'])

        self.assertEqual('test', arguments.method)

    def test_args_can_be_set(self):
        arguments = self.parser.parse(['--args', 'test'])

        self.assertIn('test', arguments.args)


class TestTemplateArgumentParser(unittest.TestCase):
    def setUp(self):
        self.parser = TemplateArgumentParser()
        self.parser.add_arguments()

    def test_overwrite_can_be_set(self):
        arguments = self.parser.parse(['--overwrite', 'yes', 'template_file', 'output_file'])

        self.assertEqual('yes', arguments.overwrite)

    def test_overwrite_defaults_to_ask(self):
        arguments = self.parser.parse(['template_file', 'output_file'])

        self.assertEqual('ask', arguments.overwrite)

    def test_template_file_can_be_set(self):
        arguments = self.parser.parse(['template_file', 'output_file'])

        self.assertEqual('template_file', arguments.template_file)

    def test_output_file_can_be_set(self):
        arguments = self.parser.parse(['template_file', 'output_file'])

        self.assertEqual('output_file', arguments.output_file)


if __name__ == '__main__':
    unittest.main()
