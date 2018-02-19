# Template

The template module allows you to render templates using the Jinja2 (see http://jinja.pocoo.org/)
template engine. It is meant to be used to create project settings files and support easy
project setup.

See common example below.

## Parameters

None so far.

## Functions provided

* **render:** Allows you to render a template. See example below.

## Template context

b5 will provide the configuration as `config` as template context. Also the full
`state` of the current b5 run will be available. Template context will look like:

```json
{"config": {"modules": {"template": None},
            "paths": {"web": "../web"},
            "project": {"key": "example",
                        "name": "Example",
                        "url": "https://www.example.com/"}},
 "state": {"args": {"command": "sometask",
                    "command_args": [],
                    "configfiles": ["~/.b5/config.yml",
                                    "config.yml",
                                    "local.yml"],
                    "detect": "git",
                    "project_path": None,
                    "run_path": "build",
                    "shell": "/bin/bash",
                    "taskfiles": ["~/.b5/Taskfile",
                                  "Taskfile",
                                  "Taskfile.local"]},
           "config": {/* see above */},
           "configfiles": [{"config": "config.yml",
                            "path": "/path/to/project/build/config.yml"}],
           "project_path": "/path/to/project/",
           "run_path": "/path/to/project/build",
           "stored_name": "/path/to/stored/state",
           "taskfiles": [{"path": "/path/to/project/build/Taskfile",
                          "taskfile": "Taskfile"}]}}
```

Normally using the config should be enough for template rendering. 

## Example usage

### Example

config.yml:
```yaml
modules:
  template:
```

Taskfile:
```bash
task:install() {
    template:render --overwrite ask-if-older templates/config.local.yml.jinja2 config.local.yml
}

task:update() {
    template:render --overwrite yes templates/settings.php.jinja2 ../web/settings.php
}
```

### template:render --help

```
usage: template:render [-h] [-o [{yes,if-older,no,ask,ask-if-older}]]
                       template_file [output_file]

positional arguments:
  template_file
  output_file

optional arguments:
  -h, --help            show this help message and exit
  -o [{yes,if-older,no,ask,ask-if-older}], --overwrite [{yes,if-older,no,ask,ask-if-older}]
                        Control if existing files should be overwritten
                        (default: ask)
```

