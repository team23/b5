# Pipenv

Handling of your virtualenv's using pipenv and pyenv. This is a better approach than using
the virtualenv module, as is uses pipenv, the
["officially recommended Python packaging tool"](https://packaging.python.org/tutorials/managing-dependencies/#managing-dependencies).

## Parameters

* **base_path:** Base path for all further paths/files. Defaults to ".", which normally means build/.
* **pipenv_bin:** Pipenv binary to be called for initializing the virtualenv. Defaults to "pipenv".
* **pyenv_bin:** Pyenv binary to be used, defaults to "pyenv".
* **use_pyenv:** You may switch of using pyenv, be aware, that no automatic installation of the required
  python version will happen without pyenv. Default to true.
* **install_dev:** Allows you to activate/deactivate dev package installation. Default to true.
* **store_venv_in_project:** Allows you to control whether the virtualenv will be put in `{base_path}/.venv` (true)
  or `$HOME/.local/share/virtualenvs/` (false). Defaults to true.
* **pipfile:** Path to Pipfile, will be searched for inside `base_path`. Defaults to "Pipfile"
  (Meaning build/Pipfile).

## Functions provided

* **install:** Initializes the virtualenv using `pipenv_bin`. Will use `pyenv_bin` to download the
  requested python version first, if `use_pyenv` is set to true (default). 
* **update:** Same as install.
* **run:** Can be used to run commands inside the virtualenv installed by pipenv, for example if command line tools were installed.
* **pipenv:** Will call `pipenv` with the modules environment, similar to using `pipenv:run pipenv …`.
* **pyenv:** Will call `pyenv` with the modules environment, similar to using `pipenv:run pyenv …`.
* **shell:** Will call `pipenv shell` with the modules environment, similar to using `pipenv:run pipenv shell …`.

## Example usage

### Example 1 - default configuration

config.yml:
```yaml
modules:
  pipenv:  # Using default configuration
```

Taskfile:
```bash
task:install() {
    pipenv:install
}

task:update() {
    pipenv:update
}

task:pipenv() {
    pipenv:pipenv "$@"
}
```

### Example Pipfile

```toml
# Defines which package repositories to use. Normally only PyPI is used.
[[source]]

url = "https://pypi.python.org/simple"
verify_ssl = true
name = "pypi"


# Normal requirements for running the project:
[packages]

pyyaml = ">=3.12"
termcolor = ">=1.1.0"
"jinja2" = ">=2.10"
markupsafe = ">=1.0"


# Additional dev dependencies. Could include the test suite. In this example
# we installed the python package itself using "pipenv install -e ."
[dev-packages]

"e1839a8" = {path = ".", editable = true}


# Required python version to use.
[requires]

python_version = "3.6"
```

