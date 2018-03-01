# Artisan

The Laravel Console.

## Parameters

* **base_path:** Base path for all further paths/files. Defaults to "../web", which normally means web/.
* **php_bin:** php binary to be used
* **artisan_bin:** artisan binary to be used

## Functions provided

* **local:** Can be used to pass any artisan command.

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
    artisan:local "$@"
}  

task:serve() {
    artisan:local serve
}

task:migrate-fresh() {
    artisan:local migrate:fresh --seed
}
```

## Roadmap

* Add docker function which supports passing artisan commands to a docker container
