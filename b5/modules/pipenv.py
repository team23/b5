import shlex
import os

from . import BaseModule


class PipenvModule(BaseModule):
    '''Pipenv module
    '''

    DEFAULT_CONFIG = {
        'base_path': '.',
        'pipenv_bin': 'pipenv',
        'pyenv_bin': 'pyenv',
    }

    def prepare_config(self):
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))

    def get_script(self):
        script = [super(PipenvModule, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_source('install', '''
            (
                cd {base_path} && \\
                {pipenv_bin} install --dev
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            pipenv_bin=shlex.quote(self.config['pipenv_bin']),
            name=self.name,
        )))

        script.append(self._script_function_source('update', '''
            {name}:install
        '''.format(
            name=self.name,
        )))

        script.append(self._script_function_source('run', '''
            (
                local initial_path="$( pwd )"
                cd "{base_path}" && \\
                eval "$( {pyenv_bin} init - )" && \\
                source "$( {pipenv_bin} --venv )/bin/activate" && \\
                cd "$initial_path" && \\
                "$@"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            pyenv_bin=self.config['pyenv_bin'],
            pipenv_bin=self.config['pipenv_bin'],
        )))

        script.append(self._script_function_source('pipenv', '''
            (
                eval "$( {pyenv_bin} init - )" && \\
                cd {base_path} && \\
                {pipenv_bin} "$@"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            pyenv_bin=self.config['pyenv_bin'],
            pipenv_bin=self.config['pipenv_bin'],
        )))

        script.append(self._script_function_source('pyenv', '''
            (
                eval "$( {pyenv_bin} init - )" && \\
                cd {base_path} && \\
                {pyenv_bin} "$@"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            pyenv_bin=self.config['pyenv_bin'],
        )))

        return '\n'.join(script)
