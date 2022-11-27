# Docker

Necessary tools to handling docker containers. Intended to be used in combination with a `docker-compose.yml`, which
you probably want to put inside build/, too.

## Parameters

* **base_path:** Base path for all further paths/files. Defaults to ".", which normally means build/.
* **docker_bin:** docker binary to be used. Defaults to "docker".
* **docker_compose_bin:** docker-compose binary to be used, defaults to "docker-compose".
* **docker_compose_configs:** List of configuration files to be used. `docker-compose` defaults to compose config files
  by default (`compose.yaml`, `compose.yml`, `docker-compose.yaml`, `docker-compose.yml`). In addition an override file
  will automatically added if found (like `compose.override.yaml`).
* **docker_compose_config_overrides:** Shortcut for adding an additional configuration files. Passing "something" will set
  `docker_compose_configs` to `compose.yaml`, `compose.something.yaml`, `compose.override.yaml`. If
  `docker_compose_configs` is set, the file `compose.something.yaml` will just be appended.You may use this
  as a list to pass multiple overrides.  
  **Note:** The actual file name depends on either the first file name used in `docker_compose_configs` or the first file
  found following the docker compose file naming convention. All overrides MUST follow the SAME naming schema. So if
  you use `docker-compose.yml` instead of `compose.yaml` the override file must be named
  `docker-compose.something.yml`.
* **docker_compose_config_override:** DEPRECATED single override form of docker_compose_config_overrides, use
  docker_compose_config_overrides instead.
* **docker_machine_bin:** docker-machine binary to be used, defaults to "docker-machine".
* **data_path:** Path to shared data folder. Might be set for further operations on this path. Defaults to None.
* **project_name:** Project name used for docker-compose. Defaults to `$config.project.key`, will fallback to projects
  path basename.
* **docker_machine:** Docker machine to be used for all docker commands. The module will set the environment
  accordingly. Defaults to None, so local docker will be used.
* **commands:** Create shortcut commands for running tasks inside the container. Uses `container_run` (see below) for
  command execution. See example below. Commands are provided as `docker:command:…`. You may use `--pipe-out` or
  `--pipe-in` to handle pipes (see `container_run`). You may use `-T` or `--disable-tty` to disable pseudo-tty
  allocation at all. All these parameters must be passed first, as other parameters will be passed to the executed
  command inside docker.
* **setup**: Allows you to tell b5 to setup some docker specific things before running docker itself. This currently
  only supports one subkey 'networks' which can be a list of networks to create (if they do not yet exist).
  There is (currently) no logic implemented to clean up these networks after they have been created by b5.
  Can be used to make sure networks marked as external exist before running docker.  
* **sync**: List of paths to sync to docker volumes. See example below. Syncing some paths into volumes may
  increase the performance significantly. Note that these paths will only be updated when calling `docker:update`
  or `docker:sync`. Internally
  [`instrumentisto/rsync-ssh`](https://hub.docker.com/r/instrumentisto/rsync-ssh) will be used to call rsync.

## Functions provided

* **install:** Calls `docker-compose build` to setup the docker images.
* **update:** Updates your docker images as `install`. In addition all sync paths will be populated (if set to
    `auto=True`).
* **run:** Can be used to run commands with the appropriate docker environment set.
* **docker:** Will call `docker` with env etc. set, similar to using `docker:run docker …`
* **docker-compose:** Will call `docker-compose` with env etc. set, similar to using `docker:run docker-compose …`
* **docker-machine:** Will call `docker-machine` with env etc. set, similar to using `docker:run docker-machine …`
* **container_run:** Will use `docker-compose` to run one single command inside a named docker container. Similar to
    using `docker:run docker-compose run --rm $CONTAINER $COMMAND`. Be aware, that `container_run` will
    use `docker:run docker-compose exec …` if the container is already running. This will reduce the necessary
    overhead to run your command. (*Note:* It will currently use `docker exec …` in reality, as `docker-compose exec`
    is [broken](https://github.com/docker/compose/issues/3352))
    
    You may use `--force-exec` or `--force-run` to force the execution model and
    skip auto-detection (note `--force-exec` will fail, if container is not running). When using this command inside
    shell pipes use `--pipe-in` (meaning `something | docker:container_run …`) or `--pipe-out`
    (meaning `docker:container_run … | something`) for easy configuration of TTY usage.  
    You may use `docker:container_run -T …` to disable pseudo-tty allocation manually, but better use
    `--pipe-in` or `--pipe-out` (instead of `-T` you may use `--disable-tty` for better readability).
    
    The following options will also be available: `-w`/`--workdir`, `-u`/`--user`, `-e`/`--env`. For `--force-run`
    the following options are available in addition:  `--no-deps`, `-l`/`--label`. See `docker`/`docker-compose`
    documentation for details.
* **is_running:** Will return 0 or 1 whether one container or any container is running. Usage: `docker:is_running`
    for checking if any container is running, `docker:is_running $SERVICE` when checking for an particular
    service. May be used like: `if $( docker:is_running ) ; then … ; fi`.
* **docker:command:…:** Will call the command you specified in the options by name. See example below.
* **sync:** Will sync your selected paths to docker volumes where `auto=true`.
* **sync:…:** Will only sync one of the configured paths. You may pass an directory name to only sync a subfolder.

## Additional environment provided when using docker:run

```bash
COMPOSE_PROJECT_NAME="project_name"  # see config above
DOCKER_HOST_SYSTEM=darwin  # linux, darwin, …
DOCKER_HOST_USERNAME=username  # local user username
DOCKER_HOST_UNIX_UID=1000  # user id
DOCKER_HOST_UNIX_GID=1000  # user group id
```

If config option "docker_machine" is set `eval $(docker-machine env "{docker_machine}")` will we executed in addition.

## Example usage

### Example 1 - default configuration

config.yml:
```yaml
modules:
  docker:  # Using default configuration
```

Taskfile:
```bash
task:install() {
    docker:install
}

task:update() {
    docker:update
}

task:run() {
    docker:docker-compose up "$@"
}

task:halt() {
    docker:docker-compose down "$@"
}

task:shell() {
    docker:container_run web /bin/bash --login
}

task:docker-compose() {
    docker:docker-compose "$@"
}
```

### Example 2 - command definition

docker-compose.yml:
```yaml
version: "3"

services:
  # minimal example, not working really
  php:
    image: php
  python:
    image: python
```

config.yml:
```yaml
modules:
  docker:
    commands:
      artisan:
        bin: artisan
        service: php
      manage.py:
        bin: ["python", "manage.py"]
        service: python
      #full_command_example:
      #  bin: COMMAND_BINARY
      #  service: COMPOSER_SERVICE
      #  force_exec: true | false
      #  force_run: true | false
      #  # Only when force_run=true
      #  no_deps: true | false
      #  # Only when force_run=true
      #  labels:
      #    label1: value1
      #    label2: value2
      #  workdir: /some/path
      #  user: USERNAME
      #  environment:
      #    env1: value1
      #    env2: value2
```

Taskfile:
```bash
task:install() { "…" }
task:update() { "…" }

task:artisan_example() {
    docker:command:artisan "…"
}

task:django_example() {
    docker:command:manage.py --pipe-out dumpdata | gzip > dump.json.gz 
}
```

### Example 3 - synchronize paths

docker-compose.yml:
```yaml
version: "3"

services:
  # minimal example, not working really
  php:
    image: php
    volumes:
      - phpvendor:/app/web/vendor

volumes:
  phpvendor:
```

config.yml:
```yaml
modules:
  docker:
    sync:
      vendor:
        from: ../web/vendor
        to: phpvendor
        delete: true
      #full_sync_example:
      #  from: VOLUME_OR_PATH
      #  to: VOLUME_OR_PATH
      #  auto: true  # automatically sync this path when docker:update or docker:sync is run (default=true)
      #  image: DOCKER_IMAGE_NAME  # uses 'instrumentisto/rsync-ssh:latest' by default, must include rsync
      #  delete: true | false
      #  chmod: 777
      #  exclude: path/to/something/
      #  OR
      #  exclude:
      #    - path/to/something/
      #    - path/to/something-else/
      #  include: path/to/something/
      #  OR
      #  include:
      #    - path/to/something/
      #    - path/to/something-else/
```

Taskfile:
```bash
task:install() { "…"; docker:install; "…" }
# "b5 update" will run "docker:sync", too
task:update() { "…"; docker:update; "…" }

task:sync() {
    # You may use "b5 sync"
    docker:sync
}

task:sync:phpvendor() {
    # You may use "b5 sync:phpvendor"
    # You also could use "b5 sync:phpvendor bin" to just sync the bin folder
    docker:sync:phpvendor "$@"
}
```


### Example 4 - auto-create networks

If external networks are defined in docker-compose.yml they are by default not auto-created by docker-compose and
using docker-compose will fail with an error message about missing these networks.

To auto-create these external networks when using docker-compose commands use the option
setup.networks and provide a list of networks to auto-create:

docker-compose.yml:
```yaml
version: "3"

services:
  # use an external network 'text_external_net'
  php:
    image: php
    networks:
      default:
      test_external_net:
      
networks:
  default:
  test_external_net:
    external: true
```

config.yml:
```yaml
modules:
  docker:
    setup:
      # networks to auto-create
      networks:
        - test_external_net
```


