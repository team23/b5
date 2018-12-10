# Configuration

## Config files

Configuration is done using YAML and should be parsed by any tools we use for building the project. This
means gulp, fabric and event the Taskfile itself need to provide the configuration for the tasks we built.

Configuration basically is done using two configuration files:

### config.yml

This file includes the main project configuration and is shared between all developers of the project.
It may therefore not include any system-specific paths and options that may differ from developer to
developer.

Common usage may include Sass paths, PostCSS configuration, deployment details and so on.

### config.local.yml

The local configuration should never be put into versioning and are purely for usage by each developer.
All configurations options here are merged with the global configuration using the following schema:

* if value under key is a dictionary, merge both
* otherwise replace the value (local overwrites global)

An example for the `config.local.yml` can be provided as `config.local.example.yml`. For more complex
usage of local configuration use the [template module](modules/template.md). See module example.

## Taskfile configuration access

Within the Taskfile b5 will take care of configuration loading and provide all options using normal bash
variables. In general all options are broken down to variables like this (prefixed with "CONFIG_").

Example config.xml:

```yaml
project:
  name: Some project
  key: example
  url: https://www.domain.com
paths:
  web: ../web
  docker_data: ../_docker_data
```

gets transformed into

```bash
CONFIG_project_name="Some project"
CONFIG_project_key="example"
CONFIG_project_url="https://www.domain.com"
CONFIG_project_KEYS=("name" "key", "url")
CONFIG_paths_web="../web"
CONFIG_paths_docker_data="../_docker_data"
CONFIG_paths_KEYS=("web" "docker_data")
```

**Note:** The `…_KEYS` are added for iterating over the configuration values - when neccessary.

## config.yml example with comments

```yaml
# This is the central configuration for all tools we use/execute. It is available inside
# the Taskfile, too. See $CONFIG_project_name for example.

# Generic project settings
project:
  # Name of the project
  # (MANDATORY)
  name: Some project
  
  # Machine readable key for the project (used as docker container name prefix)
  # (MANDATORY)
  key: project
  
  # Public domain of project
  # (MANDATORY)
  url: http://www.domain.com/
  
# Path configuration for common paths
paths:
  # Path to web/ (document root or framework root)
  # (MANDATORY)
  web: ../web
  
  # Path for database dumps, should be added to .gitignore
  db: ../_db
```

## config.local.yml example with comments

```yaml
# The local configuration might change values from the global configuration file:
project:
  # Might be neccessary when having two compies of the project running. The key is used
  # as the docker-compose project name, so we need to avoid name clashes.
  key: projectcopy
  
# All application-specific configuration should live under the key "application" and will
# normally only be set inside the local configuration:
application:
  # Example database configuration:
  database:
    host: db
    database: docker
    username: docker
    password: docker
```

**Note:** We recommend using `application` as the base key for all application-specific (database connection,
application paths, …) configuration. 

**Note:** The application configuration might be used to generate the configuration files neccessary for the
project. See [the template module](modules/template.md).

## Accessing the config in your own code (gulp, fabric, …)

Please make sure to read [the best practice for loading the config](04_config_loading.md) in your own code.
You should **NOT** merge the multiple config files yourself.
