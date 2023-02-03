import os
import pwd
import shlex
import warnings
from typing import Tuple

from ..exceptions import B5ExecutionError
from . import CONFIG_PREFIX_RE, BaseModule


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
        'sync': {},
        'setup': {},
    }

    # Valid combinations of compose filenames according to Compose File Specification
    # See https://docs.docker.com/compose/compose-file/#compose-file
    COMPOSE_CONFIG_FILENAMES = [
        ('compose', 'yaml'),
        ('compose', 'yml'),
        ('docker-compose', 'yaml'),
        ('docker-compose', 'yml'),
    ]

    def prepare_config(self) -> None:  # noqa: C901
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
        if not isinstance(self.config['sync'], dict):
            raise B5ExecutionError('docker sync has to be a dictionary')
        if not isinstance(self.config['setup'], dict):
            raise B5ExecutionError('setup has to be a dictionary')
        else:
            if 'networks' in self.config['setup']:
                if not isinstance(self.config['setup']['networks'], list):
                    raise B5ExecutionError('setup.networks has to be a list')

        # ##### CONFIGURATION MANAGEMENT #####

        # Make sure docker_compose_configs is a list
        if self.config['docker_compose_configs'] is not None:
            if not isinstance(self.config['docker_compose_configs'], list):
                self.config['docker_compose_configs'] = [self.config['docker_compose_configs']]
            for docker_compose_config in self.config['docker_compose_configs']:
                if docker_compose_config.startswith('docker-compose'):
                    warnings.warn(f'The compose file {docker_compose_config} should be renamed to '
                                  f'comply with the newest Compose File Specification. Compose implementations '
                                  f'are no longer required to support the old docker-compose naming scheme.')
        # Make sure docker_compose_config_overrides is a list if set
        if self.config['docker_compose_config_overrides'] is not None:
            if not isinstance(self.config['docker_compose_config_overrides'], list):
                self.config['docker_compose_config_overrides'] = [self.config['docker_compose_config_overrides']]
        # Add docker_compose_config_override to docker_compose_config_overrides if set
        # (+ warn user to use docker_compose_config_overrides)
        if self.config['docker_compose_config_override'] is not None:
            warnings.warn('Use docker_compose_config_overrides instead of '
                          'docker_compose_config_override (mind the plural form)')
            if isinstance(self.config['docker_compose_config_overrides'], list):
                raise B5ExecutionError('You cannot mix docker_compose_config_override '
                                       'and docker_compose_config_overrides, normally '
                                       'you have to now update your config.local.yml')
            else:
                self.config['docker_compose_config_overrides'] = [self.config['docker_compose_config_override']]

        # Find correct config file name schema
        docker_compose_configs_was_empty = True
        docker_compose_config_prefix = None
        docker_compose_config_extension = None
        if isinstance(self.config['docker_compose_configs'], list) and self.config['docker_compose_configs']:
            # Use filename and extension of FIRST passed filename -> for overrides
            docker_compose_configs_was_empty = False
            docker_compose_config_prefix, extension = os.path.splitext(self.config['docker_compose_configs'][0])
            docker_compose_config_extension = extension[1:]
        else:
            # Detect the correct filename and extension by searching for the first existing file
            for prefix, extension in self.COMPOSE_CONFIG_FILENAMES:
                if os.path.exists(os.path.join(self.config['base_path'], f'{prefix}.{extension}')):
                    self.config['docker_compose_configs'] = [f'{prefix}.{extension}']
                    docker_compose_config_prefix = prefix
                    docker_compose_config_extension = extension
                    if prefix == 'docker-compose':
                        # If compose file with old naming scheme exists, warn the user
                        warnings.warn(
                            f'The compose override file {prefix}.{extension} should be '
                            f'renamed to comply with the newest Compose File Specification. '
                            f'Compose implementations are no longer required to support the '
                            f'old docker-compose naming scheme.',
                            DeprecationWarning,
                            stacklevel=2,
                        )
                    break

        # Abort if we found no config file
        if docker_compose_config_prefix is None:
            raise B5ExecutionError('No docker compose config file found in run path. Either provide a '
                                   'valid docker compose config file '
                                   '(see https://docs.docker.com/compose/compose-file/#compose-file) or use '
                                   'the docker_compose_configs config option.')

        # Merge docker_compose_config_overrides and docker_compose_configs
        if isinstance(self.config['docker_compose_config_overrides'], list):
            for override in self.config['docker_compose_config_overrides']:
                self.config['docker_compose_configs'].append(f'{docker_compose_config_prefix}'
                                                             f'.{override}'
                                                             f'.{docker_compose_config_extension}')

        # Add default override file, if it exists
        if (
            docker_compose_configs_was_empty
            and os.path.exists(os.path.join(
                self.config['base_path'],
                f'{docker_compose_config_prefix}.override.{docker_compose_config_extension}',
            ))
        ):
            self.config['docker_compose_configs'].append(f'{docker_compose_config_prefix}'
                                                         f'.override'
                                                         f'.{docker_compose_config_extension}')

    def get_script_env(self) -> str:
        import os

        params = {
            'project_name': shlex.quote(self.config['project_name']),
            'docker_host_system': shlex.quote(os.uname().sysname.lower()),
            'docker_host_username': shlex.quote(os.getenv('LOGNAME') or pwd.getpwuid(os.getuid())[0]),
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

    def is_installed_script(self) -> str:
        """
        Add a check to evaluate whether the pipenv module bin is installed or not
        Returns: str
        """
        return self.create_is_installed_script(module=self.name, module_bin=self.config['docker_bin'])

    def _docker_volume_path_str(self, volume_path_name: str) -> Tuple[str, str]:
        # this should be a path
        if '.' in volume_path_name or '/' in volume_path_name:
            return os.path.join(self.config['base_path'], volume_path_name), 'path'
        # otherwise we handle it as a volume name
        else:
            # we do not need to add the project name
            if '_' in volume_path_name:
                return volume_path_name, 'volume'
            # construct docker compose volume name (project name + volume name)
            else:
                return '_'.join([self.config['project_name'], volume_path_name]), 'volume'

    def get_script(self) -> str:  # noqa: C901
        script = [super(DockerModule, self).get_script()]

        script.append(self._script_config_vars())

        script.append(self._script_function_source('install', '''
            {name}:compose pull
            {name}:compose build --pull
        '''.format(
            name=self.name,
        )))

        script.append(self._script_function_source('update', '''
            {name}:install
            {name}:sync
        '''.format(
            name=self.name,
        )))

        script.append(self._script_function_source('run', '''
            {name}:setup
            (
                {docker_env}
                "$@"
            )
        '''.format(
            name=self.name,
            docker_env=self.get_script_env(),
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

        script.append(self._script_function_source('compose', '''
            (
                cd {base_path} && \\
                {name}:run {docker_bin} compose {docker_compose_configs} "$@"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            name=self.name,
            docker_bin=shlex.quote(self.config['docker_bin']),
            docker_compose_configs=(
                '-f %s' % ' -f '.join(map(shlex.quote, self.config['docker_compose_configs']))
                if self.config['docker_compose_configs']
                else ''
            ),
        )))

        script.append(self._script_function_source('docker-compose', '''
            b5:warn "You are using the old docker-compose v1 callable, you should switch to use '{name}:compose'"
            b5:warn "in your Taskfile to start using docker compose v2. Note that all internal commands"
            b5:warn "like '{name}:update' already use '{name}:compose'."
            (
                cd {base_path} && \\
                {name}:run {docker_compose_bin} {docker_compose_configs} "$@"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            name=self.name,
            docker_compose_bin=shlex.quote(self.config['docker_compose_bin']),
            docker_compose_configs=(
                '-f %s' % ' -f '.join(map(shlex.quote, self.config['docker_compose_configs']))
                if self.config['docker_compose_configs']
                else ''
            ),
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

                local CONTAINER_ID="$(
                    {name}:docker ps -q \
                        --filter label=com.docker.compose.project={project_name} \
                        --filter label=com.docker.compose.service="$1" \
                    | head -n 1
                )"

                if [ -z "$CONTAINER_ID" ]
                then
                    return 1
                fi

                echo "$CONTAINER_ID"
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            project_name=shlex.quote(self.config['project_name']),
            name=self.name,
        )))

        script.append(self._script_function_source('is_running', '''
            (
                cd {base_path} || return 1

                local CONTAINER_ID=$( {name}:container_id "$1" || true )
                if [ -z "$CONTAINER_ID" ]
                then
                    return 1
                fi

                if $( docker inspect -f {{{{.State.Running}}}} "$CONTAINER_ID" )
                then
                    return 0
                else
                    return 1
                fi
            )
        '''.format(
            base_path=shlex.quote(self.config['base_path']),
            name=self.name,
        )))

        script.append(self._script_function_source('container_run', '''
            # docker-compose options
            local options=()
            local exec_options=()
            local run_options=("--rm")
            local use_tty=1

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
                        use_tty=0
                        shift
                        ;;
                    --pipe-out)
                        use_tty=0
                        shift
                        ;;
                    # Generic options
                    --disable-tty|-T)
                        use_tty=0
                        shift
                        ;;
                    -u|--user)
                        if [ -z "${{2:-}}" ]
                        then
                            b5:abort "-u can only be used with a user set (additional parameter)"
                        fi
                        options+=("-u")
                        options+=("$2")
                        shift
                        shift
                        ;;
                    -e|--env)
                        if [ -z "${{2:-}}" ]
                        then
                            b5:abort "-e can only be used with a env set (additional parameter)"
                        fi
                        options+=("-e")
                        options+=("$2")
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

            if {name}:is_running "$container"
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

            (
                cd {base_path} || return 1

                if [ $command_strategy == 'exec' ]
                then
                    {name}:compose exec "${{options[@]}}" "${{exec_options[@]}}" "$container" "$@"
                else
                    {name}:compose run "${{options[@]}}" "${{run_options[@]}}" "$container" "$@"
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
            if 'bin' not in command_options or 'service' not in command_options:
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
                        --disable-tty|-T)
                            extra_options+=("-T")
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
                    "${{extra_options[@]}}" \\
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
                        )),
                    )
                    for key, value
                    in command_options['labels'].items()
                ]) if command_options.get('labels') else '',
                workdir=(
                    '--workdir {workdir}'.format(workdir=command_options.get('workdir'))
                    if command_options.get('workdir')
                    else ''
                ),
                user=(
                    '--user {user}'.format(user=command_options.get('user'))
                    if command_options.get('user')
                    else ''
                ),
                environment=' '.join([
                    '--env {environment}'.format(
                        environment=shlex.quote('{key}={value}'.format(
                            key=key,
                            value=value,
                        )),
                    )
                    for key, value
                    in command_options['environment'].items()
                ]) if command_options.get('environment') else '',
                service=shlex.quote(command_options.get('service')),
                bin=' '.join(shlex.quote(bit) for bit in command_options.get('bin'))
                    if isinstance(command_options.get('bin'), (list, tuple))
                    else shlex.quote(command_options.get('bin')),
            )))

        if self.config['setup']:
            # Setup networks
            if 'networks' in self.config['setup'] and self.config['setup']['networks']:
                # Create a function for each network
                for setup_network_name in self.config['setup']['networks']:
                    script.append(
                        self._script_function_source(
                            'setup:network:{network}'.format(network=setup_network_name), '''
                                {name}:docker network inspect {network} &>/dev/null || (
                                    {name}:docker network create {network} && echo \"Created network {network}.\"
                                );
                            '''.format(
                                name=self.name,
                                network=shlex.quote(setup_network_name),
                            ),
                        ),
                    )
                # Create general network setup function
                script.append(self._script_function_source('setup:network', '''
                    {setup_all_networks}
                '''.format(
                    setup_all_networks='\n                    '.join([
                        '{name}:setup:network:{network}'.format(
                            name=self.name,
                            network=setup_network_name,
                        )
                        for setup_network_name
                        in self.config['setup']['networks']
                    ]),
                )))
            # Create general setup function
            setup_ran_var_name = '_{prefix}_SETUP_RAN'.format(
                prefix=CONFIG_PREFIX_RE.sub('_', self.name.upper()),
            )
            script.append('{setup_ran_var}=0'.format(setup_ran_var=setup_ran_var_name))
            setup_running_var_name = '_{prefix}_SETUP_RUNNING'.format(
                prefix=CONFIG_PREFIX_RE.sub('_', self.name.upper()),
            )
            script.append('{setup_running_var_name}=0'.format(setup_running_var_name=setup_running_var_name))
            script.append(self._script_function_source('setup', '''
                if [ "${setup_ran_var_name}" -eq 1 ]
                then
                    return 0
                fi
                if [ "${setup_running_var_name}" -eq 1 ]
                then
                    return 0
                fi
                {setup_running_var_name}=1
                {setup_networks}
                {setup_ran_var_name}=1
            '''.format(
                setup_networks=(
                    '{name}:setup:network'.format(name=self.name)
                    if 'networks' in self.config['setup'] and self.config['setup']['networks']
                    else ''
                ),
                setup_ran_var_name=setup_ran_var_name,
                setup_running_var_name=setup_running_var_name,
            )))
        else:
            # Create EMPTY general setup function, if no config exists
            script.append(self._script_function_source('setup', '''
                true
            '''))

        for sync, sync_options in self.config['sync'].items():
            if not isinstance(sync_options, dict):
                raise B5ExecutionError('sync options have to contain some options (at least "from" and "to")')
            if 'from' not in sync_options or 'to' not in sync_options:
                raise B5ExecutionError('You have to specify at least "from" and "to"')

            volume_path_from, volume_path_from_type = self._docker_volume_path_str(sync_options['from'])
            volume_path_to, volume_path_to_type = self._docker_volume_path_str(sync_options['to'])

            rsync_options = ['-grltp', '--omit-link-times']
            if 'delete' in sync_options and sync_options['delete']:
                rsync_options.append('--delete')
                rsync_options.append('--delete-after')
            if 'chmod' in sync_options and sync_options['chmod']:
                rsync_options.append('--chmod={chmod}'.format(chmod=sync_options['chmod']))
            if 'include' in sync_options and sync_options['include']:
                sync_options_includes = sync_options['include']
                if not isinstance(sync_options_includes, (list, tuple)):
                    sync_options_includes = [sync_options_includes]
                for sync_options_include in sync_options_includes:
                    rsync_options.append('--include={include}'.format(include=shlex.quote(sync_options_include)))
            if 'exclude' in sync_options and sync_options['exclude']:
                sync_options_excludes = sync_options['exclude']
                if not isinstance(sync_options_excludes, (list, tuple)):
                    sync_options_excludes = [sync_options_excludes]
                for sync_options_exclude in sync_options_excludes:
                    rsync_options.append('--exclude={exclude}'.format(exclude=shlex.quote(sync_options_exclude)))

            script.append(self._script_function_source('sync:{sync}'.format(sync=sync), '''
                local SYNC_SUBPATH=""
                if [ ! -z "${{1:-}}" ]
                then
                    SYNC_SUBPATH="$1"
                fi

                # create volumes if it does not exist
                if [ {volume_path_from_type} == "volume" ]
                then
                    local VOLUME_FROM_EXISTS="$(
                        docker volume ls \
                        | awk '{{print $2}}' \
                        | grep -Fxc {volume_path_from} || true
                    )"
                    if [ "$VOLUME_FROM_EXISTS" -eq 0 ]
                    then
                        docker volume create {volume_path_from} > /dev/null
                    fi
                fi
                if [ {volume_path_to_type} == "volume" ]
                then
                    local VOLUME_TO_EXISTS="$(
                        docker volume ls \
                        | awk '{{print $2}}' \
                        | grep -Fxc {volume_path_to} || true
                    )"
                    if [ "$VOLUME_TO_EXISTS" -eq 0 ]
                    then
                        docker volume create {volume_path_to} > /dev/null
                    fi
                fi

                # run rsync to sync data
                echo -n "Syncing files from {volume_path_from} to {volume_path_to}.."
                {name}:docker run --rm \\
                    -v {volume_path_from}:/mnt/from \\
                    -v {volume_path_to}:/mnt/to \\
                    {docker_image} \\
                    rsync  {rsync_options} "/mnt/from/$SYNC_SUBPATH" "/mnt/to/$SYNC_SUBPATH"
                echo ".done"
            '''.format(
                name=self.name,
                volume_path_from=shlex.quote(volume_path_from),
                volume_path_from_type=shlex.quote(volume_path_from_type),
                volume_path_to=shlex.quote(volume_path_to),
                volume_path_to_type=shlex.quote(volume_path_to_type),
                docker_image=(
                    shlex.quote(sync_options['image'])
                    if ('image' in sync_options and sync_options['image'])
                    else 'instrumentisto/rsync-ssh:latest'
                ),
                rsync_options=' '.join(rsync_options),
            )))

        script.append(self._script_function_source('sync', '''
            {syncs}
        '''.format(
            syncs='\n'.join(
                [
                    shlex.quote('{name}:sync:{sync}'.format(
                        name=self.name,
                        sync=sync,
                    ))
                    for sync, sync_options
                    in self.config['sync'].items()
                    if sync_options.get('auto', True)
                ],
            ) or 'true',
        )))

        return '\n'.join(script)
