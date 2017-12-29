# npm

Handling of your node packages using npm.

## Parameters

* **base_path:** Base path for all further paths/files. Defaults to ".", which normally means build/.
* **npm_bin:** npm binary to be used, defaults to "npm".

## Functions provided

* **install:** Runs `npm install` to fetch all required dependencies.
* **update:** Calls `npm update` to update the dependencies.
* **run:** Can be used to run command line tools installed inside node_modules/.
* **npm:** Will call `npm`, similar to using `npm:run npm …`

## Example usage

### Example 1 - default configuration

config.yml:
```yaml
modules:
  npm:  # Using default configuration
```

Taskfile:
```bash
task:install() {
    npm:install
}

task:update() {
    npm:update
}

task:npm() {
    npm:npm "$@"
}
```
