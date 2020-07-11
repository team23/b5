# comlipy

Handling of commit message strings.

## Parameters

* **config_path:** Configuration file path realtive to the b5 run_path. Defaults to "", which means not used.
* **comlipy_bin:** comlipy binary to be used, defaults to "comlipy".
* **comlipy_install_bin:** comlipy binary to be used for install, defaults to "comlipy-install".

## Functions provided

* **install:** Installs comlipy git commit-msg hook. Uses the comlipy-config file that has been 
defined in b5 configuration
* **update:** Updates comlipy git commit-msg hook. Uses the comlipy-config file that has been 
defined in b5 configuration. Does basically the same like comlipy:install 
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
    comlipy:update
}

task:comlipy() {
    comlipy:run "$@" || exit 1
}
```
