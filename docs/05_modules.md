# Modules

## About modules

b5 provides some common modules to allow for easy usage of generic tasks, helper functions and more. All
modules are defined inside the config.yml. Each module may be used multiple times using different parameters,
so you may for example use one virtualenv for your build/ and one for your web/ path. 

### Loading modules

Inside your config.yml you may just put the desired modules inside the "modules" key. Example:

```yaml
modules:
  modulename:
  modulewithparams:
    param1: value1
    param2: value2
```

### Naming schema

Example module: "example"

```bash
# The functions provided by the modules will be prefixed by it's name 
example:function() {
    echo "Did something"
}
```

This is important when calling module functions and for understanding how to write your own modules.

### Using modules

Some generic tasks may need to call the used modukles. This is currently used for the following tasks:
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

See source of module for details.

### legacy

Reenables legacy module loading using `b5:module_load`. Do not use.

### npm

Use npm to install JS dependencies. See [documentation](modules/npm.md).

### composer

Use composer to install PHP dependencies. See [documentation](modules/composer.md).

### virtualenv

Handling of your virtualenv's. See [documentation](modules/virtualenv.md).
