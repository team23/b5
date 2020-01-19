import argparse
from .detect import DETECT


class ArgumentParser:

    def __init__(self, prog='b5', description='', formatter_class=argparse.ArgumentDefaultsHelpFormatter):
        self.parser = argparse.ArgumentParser(
            prog=prog,
            formatter_class=formatter_class,
            description=description
        )
        self.defaults = {}

    def parse(self, arguments=None, help_as_default=False):
        if help_as_default:
            if not arguments:
                arguments = ['help']
        args = self.parser.parse_args(arguments)

        for key, value in self.defaults.items():
            if not getattr(args, key):
                setattr(args, key, value)

        return args

    def set_default(self, key, value):
        self.defaults.update({key: value})


class MainArgumentParser(ArgumentParser):
    """
        class for parsing all the b5 command line arguments.

        Possible command line argument:
        --config -c Path to config (inside run path)
        --taskfile -t Path to Taskfile (inside run path)
        --project-path -p Project path if not part of parent paths, normally b5 tries to get the project path by itself
        --run-path -r Path inside the project b5 will execute in (cd into)
        --detect -d Version Control System detection (git or hg)
        --shell -s Shell to run the generated script in (should be bash)
        --quiet -q Determine if the script should print out stuff
    """

    def add_arguments(self):
        self.__add_argument_config()
        self.__add_argument_taskfile()
        self.__add_argument_project_path()
        self.__add_argument_run_path()
        self.__add_argument_detect()
        self.__add_argument_shell()
        self.__add_argument_quiet()
        self.__add_argument_command()

    def __add_argument_config(self):
        self.parser.add_argument(
            '-c', '--config',
            nargs='?',
            action='append',
            help='Path to config (inside run path)',
            dest='configfiles',
        )

    def __add_argument_taskfile(self):
        self.parser.add_argument(
            '-t', '--taskfile',
            nargs='?',
            action='append',
            help='Path to Taskfile (inside run path)',
            dest='taskfiles',
        )

    def __add_argument_project_path(self):
        self.parser.add_argument(
            '-p', '--project-path',
            nargs='?',
            help='Project path if not part of parent paths, normally b5 tries to get the project path by itself',
            dest='project_path',
        )

    def __add_argument_run_path(self):
        self.parser.add_argument(
            '-r', '--run-path',
            nargs='?',
            help='Path inside the project b5 will execute in (cd into)',
            dest='run_path',
            default='build',
        )

    def __add_argument_detect(self):
        self.parser.add_argument(
            '-d', '--detect',
            nargs='?',
            help='Project detection',
            choices=DETECT,
            dest='detect',
            default='git',
        )

    def __add_argument_shell(self):
        self.parser.add_argument(
            '-s', '--shell', nargs='?',
            help='Shell to run the generated script in (should be bash)',
            dest='shell',
            default='/bin/bash',
        )

    def __add_argument_quiet(self):
        self.parser.add_argument(
            '-q', '--quiet',
            action='store_true',
            dest='quiet',
            default=False,
        )
        self.parser.set_defaults()

    def __add_argument_command(self):
        self.parser.add_argument('command')
        self.parser.add_argument('command_args', nargs=argparse.REMAINDER)


class InitArgumentParser(ArgumentParser):
    def add_arguments(self):
        self.__add_argument_skeleton()
        self.__add_argument_branch()
        self.__add_argument_path()

    def __add_argument_skeleton(self):
        self.parser.add_argument(
            '-s', '--skeleton',
            nargs='?',
            dest='skeleton',
            default='basic',
        )

    def __add_argument_branch(self):
        self.parser.add_argument(
            '-b', '--branch',
            nargs='?',
            dest='branch',
        )

    def __add_argument_path(self):
        self.parser.add_argument(
            dest='path'
        )


class ExecuteArgumentParser(ArgumentParser):
    def add_arguments(self):
        self.__add_argument_state_file()
        self.__add_argument_module()
        self._add_argument_method()
        self.__add_argument_args()

    def __add_argument_state_file(self):
        self.parser.add_argument(
            '--state-file', nargs='?',
            dest='state_file',
        )

    def __add_argument_module(self):
        self.parser.add_argument(
            '--module', nargs='?',
            dest='module',
        )

    def _add_argument_method(self):
        self.parser.add_argument(
            '--method', nargs='?',
            dest='method',
        )

    def __add_argument_args(self):
        self.parser.add_argument(
            '--args',
            nargs=argparse.REMAINDER,
            dest='args'
        )


class TemplateArgumentParser(ArgumentParser):
    def add_arguments(self):
        self.__add_argument_overwrite()
        self.__add_argument_template_file()
        self.__add_argument_output_file()

    def __add_argument_overwrite(self):
        self.parser.add_argument(
            '-o', '--overwrite', nargs='?',
            help='Control if existing files should be overwritten',
            dest='overwrite', default='ask',
            choices=['yes', 'if-older', 'no', 'ask', 'ask-if-older']
        )

    def __add_argument_template_file(self):
        self.parser.add_argument('template_file')

    def __add_argument_output_file(self):
        self.parser.add_argument('output_file', nargs='?')
