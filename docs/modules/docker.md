# Docker

Necessary tools to handling docker containers. Intended to be used in combination with a `docker-compose.yml`, which
you probably want to put inside build/, too.

## Parameters

* **base_path:** Base path for all further paths/files. Defaults to ".", which normally means build/.
* **docker_bin:** docker binary to be used. Defaults to "docker".
* **docker_compose_bin:** docker-compose binary to be used, defaults to "docker-compose".
* **docker_compose_configs:** List of configuration files to be used. `docker-compose` defaults to `docker-compose.yml`,
  `docker-compose.override.yml` by default. 
* **docker_compose_config_override:** Shortcut for adding an additional configuration file. Passing "something" will set
  `docker_compose_configs` to `docker-compose.yml`, `docker-compose.something.yml`, `docker-compose.override.yml`. If
  `docker_compose_configs` is set, the file `docker-compose.something.yml` will just be appended.   
* **docker_machine_bin:** docker-machine binary to be used, defaults to "docker-machine".
* **data_path:** Path to shared data folder. Might be set for further operations on this path. Defaults to None.
* **project_name:** Project name used for docker-compose. Defaults to $config.project.key, will fallback to projects
  path basename.
* **docker_machine:** Docker machine to be used for all docker commands. The module will set the environment
  accordingly. Defaults to None, so local docker will be used.

## Functions provided

* **install:** Calls `docker-compose build` to setup the docker images.
* **update:** Same as `install`.
* **run:** Can be used to run commands with the appropriate docker environment set.
* **docker:** Will call `docker` with env etc. set, similar to using `docker:run docker …`
* **docker-compose:** Will call `docker-compose` with env etc. set, similar to using `docker:run docker-compose …`
* **docker-machine:** Will call `docker-machine` with env etc. set, similar to using `docker:run docker-machine …`
* **container_run:** Will use `docker-compose` to run one single command inside a named docker container. Similar to
    using `docker:run docker-compose run --rm $CONTAINER $COMMAND`. You may use `docker:container_run -T …` to disable
    pseudo-tty allocation (Will be necessary for some tools like mysqldump). Be aware, that `container_run` will
    use `docker:run docker-compose exec …` if the container is already running. This will reduce the necessary
    overhead to run your command.
* **is_running:** Will return 0 or 1 whether one container or any container is running. Usage: `docker:is_running`
    for checking is any container is running, `docker:is_running $SERVICE` when chacking for an particular
    service. May be used like: `if $( docker:is_running ) ; then … ; fi`.

## Additional environment provided when using docker:run

```bash
COMPOSE_PROJECT_NAME="project_name"  # see config above
DOCKER_HOST_SYSTEM=darwin  # linux, darwin, …
DOCKER_HOST_USERNAME=username  # local user username
DOCKER_HOST_UNIX_UID=1000  # user id
DOCKER_HOST_UNIX_GID=1000  # user group id
```

If $config.docker_machine is set `eval $(docker-machine env "{docker_machine}")` will we executed in addition.

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

task:stop() {
    docker:docker-compose down "$@"
}

task:shell() {
    docker:container_run web /bin/bash --login
}

task:docker-compose() {
    docker:docker-compose "$@"
}
```


