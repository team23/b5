import re
import shlex
import os
import subprocess

from . import BaseModule


class PipenvModule(BaseModule):
    '''Pipenv module
    '''

    DEFAULT_CONFIG = {
        'base_path': '.',
        'pipenv_bin': 'pipenv',
        'pyenv_bin': 'pyenv',
        'use_pyenv': True,
        'install_dev': True,
        'store_venv_in_project': True,  # Sets PIPENV_VENV_IN_PROJECT to 1
        'pipfile': 'Pipfile',  # Sets PIPENV_PIPFILE
    }

    def get_version(self):
        version_string = subprocess.check_output(' '.join(['pipenv', '--version']), shell=True, env={},encoding='UTF-8')
        r = re.search(r'(\d+\.)+\d+', version_string)

        return r.group(0) if r else None

    def prepare_config(self):
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))

    def _pipenv_environment(self):
        return '''
            {pyenv_init}
            export PIPENV_VENV_IN_PROJECT="{store_venv_in_project}"
            export PIPENV_PIPFILE={pipfile}
        '''.format(
            pyenv_init='eval "$( {pyenv_bin} init - )"'.format(pyenv_bin=shlex.quote(self.config['pyenv_bin'])) \
                        if self.config['use_pyenv'] else '',
            store_venv_in_project='1' if self.config['store_venv_in_project'] else '',
            pipfile=shlex.quote(self.config['pipfile']),
        )

    def get_script(self):
        script = [super(PipenvModule, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_source('install', '''
            (
                {environment}
                cd {base_path} && \\
                {pipenv_bin} install {install_dev}
            )
        '''.format(
            environment=self._pipenv_environment(),
            base_path=shlex.quote(self.config['base_path']),
            pipenv_bin=shlex.quote(self.config['pipenv_bin']),
            install_dev='--dev' if self.config['install_dev'] else '',
        )))

        script.append(self._script_function_source('update', '''
            {name}:install
        '''.format(
            name=self.name,
        )))

        script.append(self._script_function_source('run', '''
            (
                {environment}
                local initial_path="$( pwd )"
                cd "{base_path}" && \\
                source "$( {pipenv_bin} --venv )/bin/activate" && \\
                cd "$initial_path" && \\
                "$@"
            )
        '''.format(
            environment=self._pipenv_environment(),
            base_path=shlex.quote(self.config['base_path']),
            pipenv_bin=shlex.quote(self.config['pipenv_bin']),
        )))

        script.append(self._script_function_source('pipenv', '''
            (
                {environment}
                cd {base_path} && \\
                {pipenv_bin} "$@"
            )
        '''.format(
            environment=self._pipenv_environment(),
            base_path=shlex.quote(self.config['base_path']),
            pipenv_bin=self.config['pipenv_bin'],
        )))

        script.append(self._script_function_source('pyenv', '''
            (
                {environment}
                cd {base_path} && \\
                {pyenv_bin} "$@"
            )
        '''.format(
            environment=self._pipenv_environment(),
            base_path=shlex.quote(self.config['base_path']),
            pyenv_bin=self.config['pyenv_bin'],
        )))

        script.append(self._script_function_source('shell', '''
            (
                {environment}
                cd {base_path} && \\
                {pipenv_bin} shell "$@"
            )
        '''.format(
            environment=self._pipenv_environment(),
            base_path=shlex.quote(self.config['base_path']),
            pipenv_bin=self.config['pipenv_bin'],
        )))

        return '\n'.join(script)
