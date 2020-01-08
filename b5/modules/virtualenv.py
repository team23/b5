import shlex
import os

from . import BaseModule


class VirtualenvModule(BaseModule):
    '''Virtualenv module
    '''

    DEFAULT_CONFIG = {
        'base_path': '.',
        'virtualenv_bin': 'virtualenv',
        'python_bin': 'python3',
        'env_path': 'ENV',
        'requirements_file': 'requirements.txt',
    }

    def prepare_config(self):
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))
        self.config['env_path'] = os.path.realpath(os.path.join(
            self.config['base_path'],
            self.config['env_path'],
        ))
        self.config['requirements_file'] = os.path.realpath(os.path.join(
            self.config['base_path'],
            self.config['requirements_file'],
        ))

    def get_script(self):
        script = [super(VirtualenvModule, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_source('install', '''
            (
                cd {base_path} && \\
                {virtualenv_bin} --python={python_bin} {env_path} && \\
                {name}:update
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            virtualenv_bin=shlex.quote(self.config['virtualenv_bin']),
            python_bin=shlex.quote(self.config['python_bin']),
            env_path=shlex.quote(self.config['env_path']),
            name=self.name,
        )))

        script.append(self._script_function_source('update', '''
            (
                cd {base_path} && \\
                {name}:pip install -U -r {requirements_file}
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            requirements_file=shlex.quote(self.config['requirements_file']),
            name=self.name,
        )))

        script.append(self._script_function_source('run', '''
            (
                source {activate_path} && \\
                "$@"
            )
        '''.format(
            activate_path=shlex.quote(os.path.join(
                self.config['env_path'],
                'bin',
                'activate'
            )),
        )))

        script.append(self._script_function_source('pip', '''
            {name}:run pip "$@"
        '''.format(
            name=self.name,
        )))

        return '\n'.join(script)
