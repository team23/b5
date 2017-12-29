# Virtualenv

Handling of your virtualenv's.

## Parameters

* **base_path:** Base path for all further paths/files. Defaults to ".", which normally means build/.
* **virtualenv_bin:** Virtualenv binary to be called for initializing the virtualenv. Defaults to "virtualenv".
* **python_bin:** Python binary to be used, defaults to "python3".
* **env_path:** Path to virtualenv, will be created inside `base_path`. Defaults to "ENV" (meaning build/ENV).
* **requirements_file:** Path to requirements.txt, will be searched for inside `base_path`. Defaults to "requirements.txt" (Meaning build/requirements.txt).

## Functions provided

* **install:** Initializes the virtualenv using `virtualenv_bin` and runs `pip install -r requirements.txt` to fetch
  all required dependencies.
* **update:** Calls `pip install -U -r requirements.txt` to update the dependencies.
* **run:** Can be used to run commands inside the virtualenv, for example if command line tools were installed.
* **pip:** Will call `pip` inside the virtualenv, similar to using `virtualenv:run pip …`

## Environment provided

```bash
VIRTUALENV_base_path=/path/to/project/build/
VIRTUALENV_virtualenv_bin=virtualenv
VIRTUALENV_python_bin=python3
VIRTUALENV_env_path=/path/to/project/build/ENV
VIRTUALENV_requirements_file=/path/to/project/build/requirements.txt
VIRTUALENV_KEYS=(base_path virtualenv_bin python_bin env_path requirements_file)
```

## Example usage

### Example 1 - default configuration

config.yml:
```yaml
modules:
  virtualenv:  # Using default configuration
```

Taskfile:
```bash
task:install() {
    virtualenv:install
}

task:update() {
    virtualenv:update
}

task:pip() {
    virtualenv:pip "$@"
}
```

### Example 2 - multiple usage

config.yml:
```yaml
modules:
  virtualenv_build:
    base_path: .
    requirements_file: PYTHON_REQUIREMENTS
  virtualenv_web:
    base_path: ../web
    python_bin: python2
```

Taskfile:
```bash
task:install() {
    virtualenv_build:install
    virtualenv_web:install
}

task:update() {
    virtualenv_build:update
    virtualenv_web:update
}

task:pip_build() {
    virtualenv_build:pip "$@"
}

task:pip_web() {
    virtualenv_web:pip "$@"
}
```

