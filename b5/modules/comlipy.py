import os
import shlex

from . import BaseModule


class ComlipyModule(BaseModule):
    """
    Comlipy module
    """

    DEFAULT_CONFIG = {
        'base_path': '.',
        'comlipy_bin': 'comlipy',
        'comlipy_install_bin': 'comlipy-install',
        'config_path': '',
    }

    def prepare_config(self):
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))

        if self.config['config_path']:
            self.config['config_path'] = os.path.join(self.config['base_path'], self.config['config_path'])

    def get_script(self):
        script = [super(ComlipyModule, self).get_script()]

        script.append(self._script_config_vars())

        config_param = f" -c '{self.config['config_path']}'" if self.config['config_path'] else ''
        script.append(self._script_function_source('run', '''
        (
            cd {base_path} && \\
            {comlipy_bin}{comlipy_config_param} "$@"
        )
        '''.format(
            name=self.name,
            base_path=shlex.quote(self.config['base_path']),
            comlipy_bin=self.config['comlipy_bin'],
            comlipy_config_param=config_param,
        )))

        script.append(self._script_function_source('install', '''
        (
            cd {base_path} && \\
            {comlipy_install_bin}{comlipy_config_param}
        )
        '''.format(
            name=self.name,
            base_path=shlex.quote(self.config['base_path']),
            comlipy_install_bin=self.config['comlipy_install_bin'],
            comlipy_config_param=config_param,
        )))

        return '\n'.join(script)
