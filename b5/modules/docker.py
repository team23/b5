import shlex
import os

from . import BaseModule


class DockerModule(BaseModule):
    '''docker module
    '''

    DEFAULT_CONFIG = {
        'base_path': '.',
        'docker_compose_bin': 'docker-compose',
        'data_path': None,
        'project_name': None,
    }

    def prepare_config(self):
        self.config['base_path'] = os.path.realpath(os.path.join(
            self.state.run_path,
            self.config['base_path'],
        ))
        if self.config['data_path'] is not None:
            self.config['data_path'] = os.path.realpath(os.path.join(
                self.config['base_path'],
                self.config['data_path'],
            ))
        if self.config['project_name'] is None:
            if 'project' in self.state.config and 'key' in self.state.config['project']:
                self.config['project_name'] = self.state.config['project']['key']
            else:
                self.config['project_name'] = os.path.basename(self.state.project_path)


    def get_script(self):
        script = [super(DockerModule, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_source('install', '''
            {name}:docker-compose build
        '''.format(
            name=self.name,
        )))

        script.append(self._script_function_source('update', '''
            {name}:install
        '''.format(
            name=self.name,
        )))

        script.append(self._script_function_source('run', '''
            (
                export COMPOSE_PROJECT_NAME={project_name}
                cd {base_path} && \\
                "$@"
            )
        '''.format(
            project_name=shlex.quote(self.config['project_name']),
            base_path=shlex.quote(self.config['base_path']),
        )))

        script.append(self._script_function_source('docker-compose', '''
            {name}:run {docker_compose_bin} "$@"
        '''.format(
            name=self.name,
            docker_compose_bin=shlex.quote(self.config['docker_compose_bin']),
        )))

        script.append(self._script_function_source('container_run', '''
            {name}:run run --rm "$@"
        '''.format(
            name=self.name,
        )))

        return '\n'.join(script)
