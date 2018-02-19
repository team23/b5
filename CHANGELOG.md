# dev

* TODO

# v0.11

* Error handling working as expected again (one failing command will make b5 stop further execution)
* Template module added (see https://git.team23.de/build/b5/blob/master/docs/modules/template.md)
* composer:update will now do a "composer install", as this is the right way to go here
* docker:
  - module is ready to be used
  - docker_compose_configs and docker_compose_config_override added  
    (see https://git.team23.de/build/b5-docker-traefik for usage example)
  - docker:is_running added, might be used inside the Taskfile to handle running
    state differently
  - docker:container_run will now use `docker-compose exec` if container is already
    running
* in general $module:run will no longer do a forced path switch, this will simplify usage
* Support for config.local.yml added (should be preferred over local.yml)

# v0.10

* FIRST version of python based b5 implementation
* License added, MIT/BSD
* Eat your own dog food: b5 now uses b5 for development/build tasks
* Worked on documentation
* legacy module added:  throws a warning and needs to be enabled explicitly
  - necessary to support b5_legacy module loading (`b5:module_load`)
* Better error handling
* New modules: virtualenv, npm, composer and docker (beta)
