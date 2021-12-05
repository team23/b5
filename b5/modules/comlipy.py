import os

from . import BaseModule


class ComlipyModule(BaseModule):
    """
    Comlipy module
    """

    DEFAULT_CONFIG = {
        'comlipy_bin': 'comlipy',
        'comlipy_install_bin': 'comlipy-install',
        'config_path': '',
    }

    def prepare_config(self) -> None:
        if self.config['config_path']:
            self.config['config_path'] = os.path.realpath(os.path.join(self.state.run_path, self.config['config_path']))

    def is_installed_script(self) -> str:
        """
        Add a check to evaluate whether the comlipy module bin is installed or not
        Returns: str
        """
        return self.create_is_installed_script(module=self.name, module_bin=self.config['comlipy_bin'])

    def get_script(self) -> str:
        script = [super(ComlipyModule, self).get_script()]

        script.append(self._script_config_vars())

        config_param = f" -c '{self.config['config_path']}'" if self.config['config_path'] else ''
        script.append(self._script_function_source('run', '''
        (
            {comlipy_bin}{comlipy_config_param} "$@"
        )
        '''.format(
            comlipy_bin=self.config['comlipy_bin'],
            comlipy_config_param=config_param,
        )))

        script.append(self._script_function_source('install', '''
        (
            {comlipy_install_bin}{comlipy_config_param}
        )
        '''.format(
            comlipy_install_bin=self.config['comlipy_install_bin'],
            comlipy_config_param=config_param,
        )))

        script.append(self._script_function_source('update', '''
            (
                {comlipy_install_bin}{comlipy_config_param}
            )
        '''.format(
            comlipy_install_bin=self.config['comlipy_install_bin'],
            comlipy_config_param=config_param,
        )))

        return '\n'.join(script)
