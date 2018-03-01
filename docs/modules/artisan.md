# Artisan

The Laravel Console.

## Parameters

* **base_path:** Base path for all further paths/files. Defaults to "../web", which normally means web/.
* **php_bin:** php binary to be used
* **artisan_bin:** artisan binary to be used

## Functions provided

* **run:** Can be used to pass any artisan command.

## Example usage

### Example 1 - default configuration

config.yml:
```yaml
modules:
  artisan:  # Using default configuration
```

Taskfile:
```bash
task:artisan(){
    artisan:run "$@"
}  

task:serve() {
    artisan:run serve
}

task:migrate-fresh() {
    artisan:run migrate:fresh --seed
}
```
