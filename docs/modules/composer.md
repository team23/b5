# Composer

Handling of your PHP packages using composer.

## Parameters

* **base_path:** Base path for all further paths/files. Defaults to ".", which normally means build/.
* **composer_bin:** composer binary to be used, defaults to "composer".
* **vendor_path:** Path to vendor/, necessary for calling command line tools installed by composer. Defaults to "vendor", which normally means build/vendor/.

## Functions provided

* **install:** Runs `composer install` to fetch all required dependencies.
* **update:** Calls `composer update` to update the dependencies.
* **run:** Can be used to run command line tools installed inside vendor/.
* **composer:** Will call `composer`, similar to using `composer:run composer …`

## Example usage

### Example 1 - default configuration

config.yml:
```yaml
modules:
  composer:  # Using default configuration
```

Taskfile:
```bash
task:install() {
    composer:install
}

task:update() {
    composer:update
}

task:composer() {
    composer:composer "$@"
}
```
