# Laravel

The Laravel Console. Call artisan using b5.

## Parameters

* **base_path:** Base path for all further paths/files. Defaults to "../web", which normally means web/.
* **php_bin:** php binary to be used
* **artisan_bin:** artisan binary to be used
* **docker_module:** Docker module to use when `docker_service` is set. Defaults to "docker".
* **docker_service:** Optional docker service to run command in. (**Note:** base_path will then be inside the
  docker container).

## Functions provided

* **artisan:** Can be used to pass any artisan command.

## Example usage

### Example 1 - default configuration

config.yml:
```yaml
modules:
  laravel:  # Using default configuration
```

Taskfile:
```bash
task:artisan(){
    laravel:artisan "$@"
}  

task:serve() {
    laravel:artisan serve
}

task:migrate-fresh() {
    laravel:artisan migrate:fresh --seed
}
```

## Roadmap

* Add docker function which supports passing artisan commands to a docker container
