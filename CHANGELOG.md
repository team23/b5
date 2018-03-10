# DEV

* work in progress ;-)

# v0.11.6

* b5 now uses Pipfile for dependency management, using pipenv
* pipenv module added, including some documentation
  - pipenv module includes pyenv support to install a particular python version, independent
    of the system version
* We now recommend using pipenv over virtualenv

# v0.11.5

* Added a note about additional dependencies to README.md
* Added meta information to template rendering, so templates may include something like:  

```php
<?php

/*
 * Template generated file, DO NOT EDIT.
 *
 * Original source: {{ meta.template_file }}
 * Generated: {{ meta.now }}
 */

actual_php_code();
```

# v0.11.4

* docker:container_run now uses "docker exec" instead of "docker-compose exec" when the
  container is already running. "docker-compose exec" is broken.
* Updated docker documentation to use "halt" instead of "stop"

# v0.11.3

* Pull images ob docker:install
* Write b5 error messages to stderr
* More robust docker:container_run

# v0.11.2

* Removed template module debug output
* Note to myself: No more late releases

# v0.11.1q

* Support for config.local.yml added (should be preferred over local.yml)
* Sorry, docs for v0.11 already stated to use config.local.yml, which was not true :/

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

# v0.9.0 to v0.10.5

* FIRST version of python based b5 implementation
* License added, MIT/BSD
* Eat your own dog food: b5 now uses b5 for development/build tasks
* Worked on documentation
* legacy module added:  throws a warning and needs to be enabled explicitly
  - necessary to support b5_legacy module loading (`b5:module_load`)
* Better error handling
* New modules: virtualenv, npm, composer and docker (beta)
