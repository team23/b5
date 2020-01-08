import shlex
import os

from . import BaseModule


class NpmModule(BaseModule):
    '''npm module
    '''

    DEFAULT_CONFIG = {
        'base_path': '.',
        'npm_bin': 'npm',
    }

    def prepare_config(self):
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))

    def get_script(self):
        script = [super(NpmModule, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_source('install', '''
            {name}:npm install
        '''.format(
            name=self.name,
        )))

        script.append(self._script_function_source('update', '''
            {name}:npm install
        '''.format(
            name=self.name,
        )))

        script.append(self._script_function_source('run', '''
            (
                export PATH="{base_path}/node_modules/.bin:$PATH"
                "$@"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path'])
        )))

        script.append(self._script_function_source('npm', '''
            (
                cd {base_path} && \\
                {name}:run {npm_bin} "$@"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            name=self.name,
            npm_bin=shlex.quote(self.config['npm_bin']),
        )))

        return '\n'.join(script)
