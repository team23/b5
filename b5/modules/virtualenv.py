import shlex
import os

from . import BaseModule


class VirtualenvModule(BaseModule):
    '''Virtualenv module

    Config:
        base_path: .
        python_bin: python3
        env_path: ENV
        requirements: requirements.txt
    '''

    DEFAULT_CONFIG = {
        'base_path': '.',
        'virtualenv_bin': 'virtualenv',
        'python_bin': 'python3',
        'env_path': 'ENV',
        'requirements_file': 'requirements.txt',
    }

    def get_script(self):
        script = [super(VirtualenvModule, self).get_script()]

        script.append(self._script_function_script('install', '''
            {virtualenv_bin} --python={python_bin} {env_path} && \\
            {name}:update
        '''.format(
            virtualenv_bin=shlex.quote(self.config['virtualenv_bin']),
            python_bin=shlex.quote(self.config['python_bin']),
            env_path=shlex.quote(os.path.join(
                self.state.run_path,
                self.config['base_path'],
                self.config['env_path'],
            )),
            name=self.name,
        )))

        script.append(self._script_function_script('update', '''
            {name}:pip install -U -r {requirements_file}
        '''.format(
            requirements_file=shlex.quote(os.path.join(
                self.state.run_path,
                self.config['base_path'],
                self.config['requirements_file'],
            )),
            name=self.name,
        )))

        script.append(self._script_function_script('run', '''
            (
                cd {base_path} && \\
                source {activate_path} && \\
                "$@"
            )
        '''.format(
            base_path=os.path.join(
                self.state.run_path,
                self.config['base_path'],
            ),
            activate_path=shlex.quote(os.path.join(
                self.state.run_path,
                self.config['base_path'],
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
