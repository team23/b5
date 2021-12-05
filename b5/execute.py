import os
import sys

import termcolor

from .exceptions import B5ExecutionError
from .lib.argumentparser import ExecuteArgumentParser
from .lib.module import load_module
from .lib.state import State


def main() -> None:
    try:
        parser = ExecuteArgumentParser('b5-execute', 'b5-execute is not intended to be called directly!')
        parser.add_arguments()
        args = parser.parse()

        if not args.state_file or not args.module or not args.method:
            raise B5ExecutionError('b5-execute is not intended to be called directly!')

        state = State.load(open(args.state_file, 'rb'))
        if 'modules' not in state.config:
            raise B5ExecutionError('No modules defined')
        if args.module not in state.config['modules']:
            raise B5ExecutionError('Module not available')

        module = load_module(state, args.module)
        method = getattr(module, args.method)
        if not getattr(method, 'task_executable', False):
            raise B5ExecutionError('Method not executable')

        os.chdir(state.run_path)
        method(state, args.args)
    except B5ExecutionError as error:
        termcolor.cprint(str(error), 'red')
        sys.exit(1)
