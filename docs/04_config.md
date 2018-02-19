# Configuration

# Config files

Configuration is done using YAML and should be parsed by any tools we use for building the project. This
means gulp, fabric and event the Taskfile itself need to provide the configuration for the tasks we built.

Configuration basically is done using two configuration files:

### config.yml

This file includes the main project configuration and is shared between all developers of the project.
It may therefore not include any system-specifix paths and options that may differ from developer to
developer.

Common usage may include Sass paths, PostCSS configuration, deployment details and so on. You may not
use the key "local" inside the generic configuration file.

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
paths:
  web: ../web
  docker_data: ../_docker_data
```

gets transformed into

```bash
CONFIG_paths_web="../web"
CONFIG_paths_docker_data="../_docker_data"
CONFIG_paths_KEYS=("web" "docker_data")
```

## config.yml example with comments

```yaml
# This is the central configuration for all tools we use/execute. It is parsed inside
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
  
  # Path for shared docker data, containers should get a subfolder with
  # their name in this path for persisting data.
  # Example: db-Container (MySQL) will use _docker_data/db to mount /var/lib/mysql
  # (MANDATORY - if using docker)
  #docker_data: ../_docker_data
```
