import shlex
import os

from . import BaseModule


class VirtualenvModule(BaseModule):
    '''Virtualenv module

    Config:
        python_bin: python3
        env_path: ENV
        requirements: requirements.txt
    '''

    DEFAULT_CONFIG = {
        'python_bin': 'python3',
        'env_path': 'ENV',
        'requirements_file': 'requirements.txt',
    }

    def test(self, state, args):
        print('Hello from python called via the Taskfile')
        print(args)
    test.task_executable = True

    def get_script(self):
        script = [super(VirtualenvModule, self).get_script()]

        script.append(self._script_function_script('install', '''
            virtualenv --python={python_bin} {env_path} && \\
            {name}:update
        '''.format(
            python_bin=shlex.quote(self.config['python_bin']),
            env_path=shlex.quote(os.path.join(
                self.state.run_path,
                self.config['env_path'],
            )),
            name=self.name,
        )))

        script.append(self._script_function_script('update', '''
            {name}:pip install -U -r {requirements_file}
        '''.format(
            requirements_file=shlex.quote(self.config['requirements_file']),
            name=self.name,
        )))

        script.append(self._script_function_script('run', '''
            (
                cd {run_path} && \\
                source {activate_path} && \\
                "$@"
            )
        '''.format(
            run_path=self.state.run_path,
            activate_path=shlex.quote(os.path.join(
                self.config['env_path'],
                'bin',
                'activate'
            )),
        )))

        script.append(self._script_function_script('pip', '''
            {name}:run pip "$@"
        '''.format(
            name=self.name,
        )))

        return '\n'.join(script)
