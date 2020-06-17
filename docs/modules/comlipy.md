# comlipy

Handling of commit message strings.

## Parameters

* **base_path:** Base path for all further paths/files. Defaults to ".", which normally means build/.
* **config_path:** Configuration file path realtive to `base_path`. Defaults to "", which means not used.
* **comlipy_bin:** comlipy binary to be used, defaults to "comlipy".
* **comlipy_install_bin:** comlipy binary to be used for install, defaults to "comlipy-install".

## Functions provided

* **install:** Installs comlipy git commit-msg hook. Uses the comlipy-config file that has been 
defined in b5 configuration
* **run:** Can be used to run comlipy itself. Uses the comlipy-config file that has been 
defined in b5 configuration

## Example usage

### Example

config.yml:

```yaml
modules:
  comlipy:
    config_path: 'path-to-config-file.yml'
```

Taskfile:

```bash
task:install() {
    # ...
    comlipy:install
}

task:update() {
    # ...
    comlipy:install
}

task:comlipy() {
    comlipy:run "$@" || exit 1
}
```
