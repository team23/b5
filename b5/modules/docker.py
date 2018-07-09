import shlex
import os
import warnings

from ..exceptions import B5ExecutionError
from . import BaseModule


class DockerModule(BaseModule):
    '''docker module
    '''

    DEFAULT_CONFIG = {
        'base_path': '.',
        'docker_bin': 'docker',
        'docker_compose_bin': 'docker-compose',
        'docker_compose_configs': None,
        'docker_compose_config_override': None,
        'docker_compose_config_overrides': None,
        'docker_machine_bin': 'docker-machine',
        'data_path': None,
        'project_name': None,
        'docker_machine': None,
        'commands': {},
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
        if not isinstance(self.config['commands'], dict):
            raise B5ExecutionError('docker commands has to be a dictionary')

        ##### CONFIGURATION MANAGEMENT #####

        # make sure docker_compose_configs is a list
        if self.config['docker_compose_configs'] is not None:
            if not isinstance(self.config['docker_compose_configs'], list):
                self.config['docker_compose_configs'] = [self.config['docker_compose_configs']]
        # make sure docker_compose_config_overrides is a list if set
        if self.config['docker_compose_config_overrides'] is not None:
            if not isinstance(self.config['docker_compose_config_overrides'], list):
                self.config['docker_compose_config_overrides'] = [self.config['docker_compose_config_overrides']]
        # add docker_compose_config_override to docker_compose_config_overrides if set
        # (+ warn user to use docker_compose_config_overrides)
        if self.config['docker_compose_config_override'] is not None:
            warnings.warn('Use docker_compose_config_overrides instead of docker_compose_config_override (mind the plural form)')
            if isinstance(self.config['docker_compose_config_overrides'], list):
                # self.config['docker_compose_config_overrides'].append(self.config['docker_compose_config_override'])
                raise B5ExecutionError('You cannot mix docker_compose_config_override and docker_compose_config_overrides, '
                                       'normally you have to now update your config.local.yml')
            else:
                self.config['docker_compose_config_overrides'] = [self.config['docker_compose_config_override']]
        # merge docker_compose_config_overrides and docker_compose_configs
        if isinstance(self.config['docker_compose_config_overrides'], list):
            docker_compose_configs_was_empty = False
            if not isinstance(self.config['docker_compose_configs'], list):
                docker_compose_configs_was_empty = True
                self.config['docker_compose_configs'] = ['docker-compose.yml']
            for override in self.config['docker_compose_config_overrides']:
                self.config['docker_compose_configs'].append('docker-compose.%s.yml' % override)
            if docker_compose_configs_was_empty and os.path.exists(os.path.join(self.config['base_path'], 'docker-compose.override.yml')):
                self.config['docker_compose_configs'].append('docker-compose.override.yml')

    def get_script_env(self):
        import os

        params = {
            'project_name': shlex.quote(self.config['project_name']),
            'docker_host_system': shlex.quote(os.uname().sysname.lower()),
            'docker_host_username': shlex.quote(os.getlogin()),
            'docker_host_unix_uid': '',
            'docker_host_unix_gid': '',
            'docker_machine_env': '',
        }
        if params['docker_host_system'] in ('linux', 'darwin'):
            params.update({
                'docker_host_unix_uid': shlex.quote(str(os.getuid())),
                'docker_host_unix_gid': shlex.quote(str(os.getgid())),
            })
        if self.config['docker_machine']:
            params.update({
                'docker_machine_env': 'eval $(docker-machine env %s)' % shlex.quote(self.config['docker_machine']),
            })

        return '''
            export COMPOSE_PROJECT_NAME={project_name}
            export DOCKER_HOST_SYSTEM={docker_host_system}
            export DOCKER_HOST_USERNAME={docker_host_username}
            export DOCKER_HOST_UNIX_UID={docker_host_unix_uid}
            export DOCKER_HOST_UNIX_GID={docker_host_unix_gid}
            {docker_machine_env}
        '''.format(**params)

    def get_script(self):
        script = [super(DockerModule, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_source('install', '''
            {name}:docker-compose pull
            {name}:docker-compose build --pull
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
                {docker_env}
                "$@"
            )
        '''.format(
            docker_env=self.get_script_env(),
            base_path=shlex.quote(self.config['base_path']),
        )))

        script.append(self._script_function_source('docker', '''
            (
                cd {base_path} && \\
                {name}:run {docker_bin} "$@"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            name=self.name,
            docker_bin=shlex.quote(self.config['docker_bin']),
        )))

        script.append(self._script_function_source('docker-compose', '''
            (
                cd {base_path} && \\
                {name}:run {docker_compose_bin} {docker_compose_configs} "$@"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            name=self.name,
            docker_compose_bin=shlex.quote(self.config['docker_compose_bin']),
            docker_compose_configs='-f %s' % ' -f '.join(map(shlex.quote, self.config['docker_compose_configs'])) \
                                    if self.config['docker_compose_configs'] else '',
        )))

        script.append(self._script_function_source('docker-machine', '''
            (
                cd {base_path} && \\
                {name}:run {docker_machine_bin} "$@"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            name=self.name,
            docker_machine_bin=shlex.quote(self.config['docker_machine_bin']),
        )))

        script.append(self._script_function_source('container_id', '''
            (
                cd {base_path} || return 1

                {name}:docker-compose ps -q "$@" | awk 'NR == 1'
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            name=self.name,
        )))

        script.append(self._script_function_source('is_running', '''
            (
                cd {base_path} || return 1
                local CONTAINER=$({name}:container_id dev)
                # echo "ContaineR " $({name}:container_id dev)
                local RUNNING=$(docker inspect -f {{{{.State.Running}}}} $CONTAINER)

                if $RUNNING
                    then
                        return 1
                    else
                        return 0
                fi
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            name=self.name,
            docker_machine_bin=shlex.quote(self.config['docker_machine_bin']),
        )))

        # See https://github.com/docker/compose/issues/3352 for why we are not using docker-compose exec here,
        # this basically is broken on many levels. See for example this comment:
        # https://github.com/docker/compose/issues/3352#issuecomment-299868032
        script.append(self._script_function_source('container_run', '''
            # docker-compose options
            local options=()
            local exec_options=()
            local run_options=("--rm")
            local use_tty=1
            # raw docker options (prefix "d_")
            local d_options=()
            local d_exec_options=()
            local d_run_options=("--rm")
            local d_use_tty=1

            local has_valid_options=1
            local force_run=0
            local force_exec=0

            # Parse command line options
            while [ $has_valid_options -gt 0 ]
            do
                case "${{1:-}}" in
                    # Own options
                    --force-run)
                        force_run=1
                        shift
                        ;;
                    --force-exec)
                        force_exec=1
                        shift
                        ;;
                    --pipe-in)
                        d_options+=("-i")
                        d_use_tty=0
                        shift
                        ;;
                    --pipe-out)
                        d_use_tty=0
                        use_tty=0
                        shift
                        ;;
                    # Generic options
                    -T)
                        use_tty=0
                        d_use_tty=0
                        shift
                        ;;
                    -u|--user)
                        if [ -z "${{2:-}}" ]
                        then
                            b5:abort "-u can only be used with a user set (additional parameter)"
                        fi
                        options+=("-u")
                        options+=("$2")
                        d_options+=("-u")
                        d_options+=("$2")
                        shift
                        ;;
                    -e|--env)
                        if [ -z "${{2:-}}" ]
                        then
                            b5:abort "-e can only be used with a env set (additional parameter)"
                        fi
                        options+=("-e")
                        options+=("$2")
                        d_options+=("-e")
                        d_options+=("$2")
                        shift
                        shift
                        ;;
                    -w|--workdir)
                        if [ -z "${{2:-}}" ]
                        then
                            b5:abort "-w can only be used with a path set (additional parameter)"
                        fi
                        options+=("-w")
                        options+=("$2")
                        d_options+=("-w")
                        d_options+=("$2")
                        shift
                        shift
                        ;;
                    # RUN options
                    --no-deps)
                       run_options+=("--no-deps")
                       force_run=1
                       shift
                       ;;
                    -l|--label)
                        if [ -z "${{2:-}}" ]
                        then
                            b5:abort "-l can only be used with a label set (additional parameter)"
                        fi
                        options+=("-l")
                        options+=("$2")
                        d_options+=("-l")
                        d_options+=("$2")
                        force_run=1
                        shift
                        shift
                        ;;
                    *)
                      has_valid_options=0
                      ;;
                esac
            done

            # Parse container name
            local container="${{1:-}}"
            shift
            if [ -z "$container" ]
            then
                b5:error "You need to pass the container name"
                return 1
            fi

            # Decide which strategy to use
            local command_strategy='run'
            {name}:is_running "$container"
            if [ $? -eq 1 ]
            then
                command_strategy='exec'
            fi
            if [ $force_exec -gt 0 ]
            then
                command_strategy='exec'
                if ! {name}:is_running "$container"
                then
                    b5:abort "exec not possible as container is not running"
                fi
            fi
            if [ $force_run -gt 0 ]
            then
                command_strategy='run'
            fi
            if [ $force_exec -gt 0 ] && [ $force_run -gt 0 ]
            then
                b5:abort "Trying to force run and exec, not possible"
            fi

            # Finalize options
            if [ $use_tty -lt 1 ]
            then
                options+=("-T")
            fi
            if [ $d_use_tty -gt 0 ]
            then
                d_options+=("-it")
            fi

            (
                cd {base_path} || return 1

                if [ $command_strategy == 'exec' ]
                then
                    local container_id=$( {name}:docker-compose ps -q "$container" | head -n 1 )
                    {name}:docker exec "${{d_options[@]}}" "${{d_exec_options[@]}}" "$container_id" "$@"
                else
                    {name}:docker-compose run "${{options[@]}}" "${{run_options[@]}}" "$container" "$@"
                fi
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            name=self.name,
        )))

        for command, command_options in self.config['commands'].items():
            if command_options is None:
                command_options = {'bin': command, 'service': command}
            elif isinstance(command_options, str):
                command_options = {'bin': command, 'service': command_options}
            if not 'bin' in command_options or not 'service' in command_options:
                raise B5ExecutionError('You have to specify at least "bin" and "service"')

            script.append(self._script_function_source('command:{command}'.format(command=command), '''
                local has_valid_options=1
                local extra_options=()
                while [ $has_valid_options -gt 0 ]
                do
                    case "${{1:-}}" in
                        --pipe-in)
                            extra_options+=("--pipe-in")
                            shift
                            ;;
                        --pipe-out)
                            extra_options+=("--pipe-out")
                            shift
                            ;;
                        *)
                          has_valid_options=0
                          ;;
                    esac
                done

                {name}:container_run \\
                    {force_exec} \\
                    {force_run} {no_deps} {labels} \\
                    "${{d_options[@]}}" \\
                    {workdir} {user} {environment} \\
                    {service} \\
                    {bin} "$@"
            '''.format(
                name=self.name,
                force_exec='--force-exec' if command_options.get('force_exec') else '',
                force_run='--force-run' if command_options.get('force_run') else '',
                no_deps='--no-deps' if command_options.get('no_deps') else '',
                labels=' '.join([
                    '--label {label}'.format(
                        label=shlex.quote('{key}={value}'.format(
                            key=key,
                            value=value,
                        ))
                    )
                    for key, value
                    in command_options['labels'].items()
                ]) if command_options.get('labels') else '',
                workdir='--workdir {workdir}'.format(workdir=command_options.get('workdir')) if command_options.get('workdir') else '',
                user='--user {user}'.format(user=command_options.get('user')) if command_options.get('user') else '',
                environment=' '.join([
                    '--env {environment}'.format(
                        environment=shlex.quote('{key}={value}'.format(
                            key=key,
                            value=value,
                        ))
                    )
                    for key, value
                    in command_options['environment'].items()
                ]) if command_options.get('environment') else '',
                service=shlex.quote(command_options.get('service')),
                bin=' '.join(shlex.quote(bit) for bit in command_options.get('bin'))
                    if isinstance(command_options.get('bin'), (list, tuple))
                    else shlex.quote(command_options.get('bin')),
            )))

        return '\n'.join(script)
