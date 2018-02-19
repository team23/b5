import argparse
import os
import termcolor
import sys

from .lib.state import State
from .lib.module import load_module
from .exceptions import B5ExecutionError


def main():
    try:
        parser = argparse.ArgumentParser(
            prog='b5-execute',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='b5-execute is not intended to be called directly!',
        )
        parser.add_argument(
            '--state-file', nargs='?',
            dest='state_file',
        )
        parser.add_argument(
            '--module', nargs='?',
            dest='module',
        )
        parser.add_argument(
            '--method', nargs='?',
            dest='method',
        )
        parser.add_argument(
            '--args', nargs=argparse.REMAINDER,
            dest='args'
        )
        args = parser.parse_args()

        if not args.state_file or not args.module or not args.method:
            raise B5ExecutionError('b5-execute is not intended to be called directly!')

        state = State.load(open(args.state_file, 'rb'))
        if not 'modules' in state.config:
            raise B5ExecutionError('No modules defined')
        if not args.module in state.config['modules']:
            raise B5ExecutionError('Module not available')

        module = load_module(state, args.module)
        method = getattr(module, args.method)
        if not getattr(method, 'task_executable', False):
            raise B5ExecutionError('Method not executable')

        os.chdir(state.run_path)
        method(state, args.args)
    except B5ExecutionError as e:
        termcolor.cprint(str(e), 'red')
        sys.exit(1)
