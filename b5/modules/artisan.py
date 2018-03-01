import shlex
import os

from . import BaseModule


class ArtisanModule(BaseModule):
    '''artisan module
    '''

    DEFAULT_CONFIG = {
        'base_path': '../web',
        'php_bin': 'php',
        'artisan_bin': 'artisan',
    }

    def prepare_config(self):
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))

    def get_script(self):
        script = [super(ArtisanModule, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_source('run', '''
            (
                cd {base_path} && \\
                {php_bin} {artisan_bin} "$@"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            php_bin=shlex.quote(self.config['php_bin']),
            artisan_bin=shlex.quote(self.config['artisan_bin'])
        )))

        return '\n'.join(script)
