import shlex
import os

from . import BaseModule


class ComposerModule(BaseModule):
    '''Composer module
    '''

    DEFAULT_CONFIG = {
        'base_path': '.',
        'composer_bin': 'composer',
        'vendor_path': 'vendor',
    }

    def prepare_config(self):
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))

        self.config['vendor_path'] = os.path.realpath(os.path.join(
            self.config['base_path'],
            self.config['vendor_path'],
        ))

    def get_script(self):
        script = [super(ComposerModule, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_source('install', '''
            {name}:composer install
        '''.format(
            name=self.name,
        )))

        script.append(self._script_function_source('update', '''
            {name}:composer update
        '''.format(
            name=self.name,
        )))

        script.append(self._script_function_source('run', '''
            (
                export PATH="{vendor_path}/bin/:$PATH"
                cd {base_path} && \\
                "$@"
            )
        '''.format(
            vendor_path=shlex.quote(self.config['vendor_path']),
            base_path=shlex.quote(self.config['base_path']),
        )))

        script.append(self._script_function_source('composer', '''
            {name}:run {composer_bin} "$@"
        '''.format(
            name=self.name,
            composer_bin=shlex.quote(self.config['composer_bin']),
        )))

        return '\n'.join(script)
