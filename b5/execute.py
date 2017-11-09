import argparse
import os

from .lib.module import module_load
from .lib.config import load_config


def main():
    parser = argparse.ArgumentParser(
        prog='b5e',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='b5e is not intended to be called directly!'
    )
    parser.add_argument(
        '--project-path', nargs='?',
        dest='project_path',
    )
    parser.add_argument(
        '--run-path', nargs='?',
        dest='run_path',
    )
    parser.add_argument(
        '--module', nargs='?',
        dest='module',
    )
    parser.add_argument(
        '--method', nargs='?',
        dest='method',
    )
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if not args.project_path or not args.run_path or not args.module or not args.method:
        raise RuntimeError('b5e is not intended to be called directly!')

    config = load_config(args.run_path)

    if not 'modules' in config:
        raise RuntimeError('No modules defined')
    if not args.module in config['modules']:
        raise RuntimeError('Module not available')

    module_config = config['modules'][args.module]
    module = module_load(args.project_path, args.run_path, args.module, module_config, config)
    method = getattr(module, args.method)
    if not getattr(method, 'task_executable', False):
        raise RuntimeError('Method not executable')

    os.chdir(args.run_path)
    method(args.args)
