# DEV

* work in progress ;-)

# 1.4.0 - PREPARATION, NOT RELEASED YET

* BREAKING: b5 now requires at least Python 3.8.1.
* Updated all dependencies to their latest versions.
* BREAKING: b5 will require to have a docker compose config file available for config file name detection. See
  https://docs.docker.com/compose/compose-file/#compose-file for details about the new naming schema. If you cannot
  provide an appropriate file (for example in skeletons), you may use the option `docker_compose_configs` to provide
  a file name. The first file name provided here will determine the config file prefix and extension used for
  `docker_compose_config_overrides`.
* b5 will now also support config files ending in `.yaml`. Loading config files ending in `.yml` will be deprecated
  in the future. Also note that the old `local.yml` local config file is not supported as `local.yaml` - as you should
  use `config.local.y(a)ml` instead for some time now. Thanks to Andreas Rau for noticing the
  [missing support for `.yaml` files](https://git.team23.de/build/b5/-/issues/4).

# 1.3.5

* Fix version number in code 🙈

# 1.3.4

* Fix regression with docker compose config file name detection. When no file is found in the current directory, 
  the old default file name is now used (`docker-compose.yml`). This will change in b5 1.4.0.

# 1.3.3

* You now can get a raw task list using `b5 --quiet help --tasks`
* Support for new docker compose path spec (see https://docs.docker.com/compose/compose-file/#compose-file)

# 1.3.2

* Fix issue with docker compose needing `-T` for all pipes now (docker compose 2.2.3 seems to have introduced this)

# 1.3.1

* Fix issue that `docker compose` is not always called using the internal structures and thus may miss config overrides

# 1.3.0

* b5 now used flake8 for better code quality
* All code now contains type annotations
* Support for docker compose v2 (and usage "docker compose" instead of "docker-compose")
* Update all dependencies to their current version

# 1.2.1

* Add packaging dependency again (sorry!)

# 1.2.0

* Update all dependencies to their current version
* New 'docker compose ps' does not allow filter by service name, work around this

# 1.1.9

* Packaging fixes

# 1.1.8

* Better handling for keyboard interrupt
* New comlipy module (thanks to Emanuel Jacob)
* Only show stacktrace when --traceback was used
* Docker module can now automatically create networks, can be used to have multi-project networks automatically created
* Modules now check, that required binary is installed (using which)

# 1.1.7

* Packaging fixes

# 1.1.6

* dephell did not convert console_scripts, readding this to pyproject.toml

# 1.1.5

* Use poetry for package management
* Included first test + linting
* Rewrite of argument parsing
* Better support for detecting how to clone skel repositories
* Support Python 3.8

# 1.1.4

* Docker sync config allows to specify `auto: false` to not automatically sync on `docker:update` and `docker:sync`,
  you may still use `docker:sync:$NAME` for manual synchronization 

# 1.1.3

* Docker sync feature should be much more stable now
* Docker sync options added: chmod, exclude, include
* Docker sync now allows to use volume or path on both sides  
  (you could also sync something to your outer host filesystem)

# 1.1.2

* Updates dependencies, so we use safe version of PyYAML 

# 1.1.1

* Fixed docker:sync being empty when no sync options are set (bash syntax error) 

# 1.1.0

* Make sure b5 env export does not fail on non-string lists (skipping these lists now)
* Fix `os.getlogin()` not working on Ubuntu
* Fix `docker:command:…` not handling `--pipe-in` and `--pipe-out`
* Allow to use `-T` to disable pseudo-tty on `docker:command:…`
* Added alias for `-T`: `--disable-tty` (better readability of scripts)
* docker module got sync option to automatically sync local paths to volumes - may increase performance a lot!
  (see docs for details)

# 1.0.2

* Support for specifying the necessary b5 version in config.yml
* More work on documentation

# 1.0.0

* First real release for PyPI
* 1.0! ;-)
* A lot of new and restructured documentation

# 0.13.3

* Provide ENV inside template rendering (`{{ env.SOMETHING }}`)

# 0.13.2

* Fixed docker:is_running not returning the right state

# 0.13.1

* Fixed docker:container_run not handling --user correctly
* Updated PyYAML to at least 3.13 (Python 3.7 compatibility - without beta package)

# 0.13.0

* Python 3.7 compatibility (PyYAML 3.13b1 - still not stable, but working)

# 0.12.2

* Throw error when docker_compose_config_overrides and docker_compose_config_override is mixed together, this will
  minimize usage errors due to updated projects but not updated local configs
* git-init now allows you to specify the branch to use for new projects
* git-init will clone using the SSH URL by default

# 0.12.1

* b5-init now calls "b5 project:init" instead of "b5 init" for project initialization (reduces headaches)

# 0.12.0

* b5-init readded, this allows you to create new projects using predefined skeletons (aka "templates")
* "basic" template is provided by https://git.team23.de/build/b5-skel-basic

# 0.11.10

* Added docker:command:… shortcut for running commands inside docker (see `commands` configuration
  option)
* Handle keyboard interups in a better way, not showing failed task

# v0.11.9

* export B5_STATE_FILE for access to STATE_FILE in subshells and similar
* pipenv not uses right environment even on pipenv:install/update
* docker_compose_config_overrides added to allow multiple overrides
  (will replace docker_compose_config_override, currently just a warning is shown)

# v0.11.8

* Use "docker-compose build --pull", so newer versions of images are always pulled upon build
* Serialize boolean values as 0/1 for bash

# v0.11.7

* Fixed docker exec not keeping the stream open, so shell execution breaks

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

# v0.11.1

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
