import shlex
import os

from . import BaseModule


class LaravelModule(BaseModule):
    '''Laravel module
    '''

    DEFAULT_CONFIG = {
        'base_path': '../web',
        'php_bin': 'php',
        'artisan_bin': 'artisan',
        'docker_module': 'docker',
        'docker_service': None,
    }

    def prepare_config(self):
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))

    def get_script(self):
        script = [super(LaravelModule, self).get_script()]

        script.append(self._script_config_vars())

        if self.config['docker_service'] is None:
            script.append(self._script_function_source('artisan', '''
                (
                    cd {base_path} && \\
                    {php_bin} {artisan_bin} "$@"
                )
            '''.format(
                base_path=shlex.quote(self.config['base_path']),
                php_bin=shlex.quote(self.config['php_bin']),
                artisan_bin=shlex.quote(self.config['artisan_bin'])
            )))
        else:
            script.append(self._script_function_source('artisan', '''
                {docker_module}:container_run -w {base_path} {docker_service} {php_bin} {artisan_bin} "$@"
            '''.format(
                docker_module=self.config['docker_module'],
                base_path=shlex.quote(self.config['base_path']),
                docker_service=shlex.quote(self.config['docker_service']),
                php_bin=shlex.quote(self.config['php_bin']),
                artisan_bin=shlex.quote(self.config['artisan_bin'])
            )))

        return '\n'.join(script)
