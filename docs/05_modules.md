# Modules

## About modules

b5 provides some common modules to allow for easy usage of generic tasks, helper functions and more. All
modules are defined inside the config.yml. Each module may be used multiple times using different parameters,
so you may for example use one virtualenv for your build/ and one for your web/ path. 

### Loading modules

Inside your config.yml you may just put the desired modules inside the "modules" key. Example:

```yaml
modules:
  examplemodule:
  modulewithparams:
    param1: value1
    param2: value2
```

### Naming schema

Example module: "example"

```bash
# The functions provided by the modules will be prefixed by it's name 
examplemodule:function() {
    echo "Did something"
}
```

This is important when calling module functions and for understanding how to write your own modules.

### Provided environment

All parameters passed to the module will be available in the bash environment using the following schema:
`{MODULE_NAME}_{variable_key}`

The example above will generate the following environment for `modulewithparams`:
```bash
MODULEWITHPARAMS_param1="value1"
MODULEWITHPARAMS_param2="value2"
```

Please note, that the provided environment will represent the internal values of the module. This
means that in most cases some preprocessing/cleanup of values might have happened. For paths
this for example may mean the paths are converted to absolute paths. This means:

```yaml
modules:
  example:
    some_path: ../web
```

Will most certainly become:

```bash
EXAMPLE_some_path="/absolute/path/to/project/web"
```


### Using modules

Some generic tasks may need to call the used modules. This is currently used for the following tasks:
* install
* update
* clean

Your install task may look like:

```bash
task:install() {
    virtualenv:install
    npm:install
}
```

### Using modules multiple times

If you need to use the same module twice or more (for example when needing multiple virtualenv directories)
you may need to instantiate the same module twice. This may be done using the "class" key inside the
module parameters:

```yaml
modules:
  virtualenv_build:
    class: virtualenv
    base_path: .
  virtualenv_web:
    class: virtualenv
    base_path: ../web
```

The Taskfile will then look like this:

```bash
task:install() {
    virtualenv_build:install
    virtualenv_web:install
}
```

The following environment will be provided in this case:

```bash
VIRTUALENV_BUILD_base_path="/path/to/project/build"
VIRTUALENV_BUILD_...="more variables of virtualenv module"
VIRTUALENV_WEB_base_path="/path/to/project/web"
VIRTUALENV_WEB_...="more variables of virtualenv module"
```

### Example

#### config.yml

```yaml
modules:
  npm:
  virtualenv_build:
    class: virtualenv
    base_path: .
  virtualenv_web:
    class: virtualenv
    base_path: ../web
```

```bash
#!/usr/bin/env bash
# b5 Taskfile, see https://git.team23.de/build/b5 for details

task:install() {
    npm:install
    virtualenv_build:install
    virtualenv_web:install
}

task:update() {
    npm:update
    virtualenv_build:update
    virtualenv_web:update
}

task:example() {
    echo "This is a minimal example task"
}
```

You may now use `b5 install` to install your npm and python packages, `b5 update` for updating the installed
packages.

## Existing modules

**Note:** See source of module for details, beyond documentation.

### legacy

Reenables legacy module loading using `b5:module_load`. Do not use.

### npm

Use npm to install JS dependencies. See [documentation](modules/npm.md).

### composer

Use composer to install PHP dependencies. See [documentation](modules/composer.md).

### docker

Allow simple usage of docker. See [documentation](modules/docker.md).

### pipenv

Handling of your virtualenv's using pipenv. See [documentation](modules/pipenv.md).

### virtualenv

Handling of your virtualenv's. See [documentation](modules/virtualenv.md).

### template

Allows for easy template rendering using Jinja2. See [documentation](modules/template.md).
