import os
import shlex

from . import BaseModule


class ComposerModule(BaseModule):
    '''Composer module
    '''

    DEFAULT_CONFIG = {
        'base_path': '.',
        'composer_bin': 'composer',
        'vendor_path': 'vendor',
    }

    def prepare_config(self) -> None:
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))
        self.config['vendor_path'] = os.path.realpath(os.path.join(
            self.config['base_path'],
            self.config['vendor_path'],
        ))

    def is_installed_script(self) -> str:
        """
        Add a check to evaluate whether the pipenv module bin is installed or not
        Returns: str
        """
        return self.create_is_installed_script(module=self.name, module_bin=self.config['composer_bin'])

    def get_script(self) -> str:
        script = [super(ComposerModule, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_source('install', '''
            {name}:composer install
        '''.format(
            name=self.name,
        )))

        # "composer install" will update the dependencies, "composer update" will
        # upgrade the installed version. So we use "composer install" here, too.
        script.append(self._script_function_source('update', '''
            {name}:composer install
        '''.format(
            name=self.name,
        )))

        script.append(self._script_function_source('run', '''
            (
                export PATH="{vendor_path}/bin/:$PATH"
                "$@"
            )
        '''.format(
            vendor_path=shlex.quote(self.config['vendor_path']),
        )))

        script.append(self._script_function_source('composer', '''
            (
                cd {base_path} && \\
                {name}:run {composer_bin} "$@"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            name=self.name,
            composer_bin=shlex.quote(self.config['composer_bin']),
        )))

        return '\n'.join(script)
