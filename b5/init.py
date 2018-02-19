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
            prog='b5-init',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='b5-init might be used to setup new projects',
        )
        parser.add_argument(
            '-t', '--template', nargs='?',
            dest='template', default='minimal'
        )
        args = parser.parse_args()

        raise B5ExecutionError('This is not ready yet')
    except B5ExecutionError as e:
        termcolor.cprint(str(e), 'red')
        sys.exit(1)
