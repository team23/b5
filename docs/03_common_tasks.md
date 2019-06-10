# Tasks we use as TEAM23

The following tasks are required to work as described below for every project and should be available if
necessary.

## Project setup

### install

Side note: `install` has formerly be known as `setup` (`fab setup`).

The install task will setup the project for you. It will install dependencies (npm, virtualenv, …), and
make sure an initial config exists.

You may need to update `config.local.yml` after initially running this tasks and then run `b5 update` to (re)create
the application config.

### update

When working on a project you may at some time introduce changes that might break the installation
of the project for your colleges. This might include changing the database schema, add additional
configuration options, …

`b5 update` will use the necessary tools to make sure the project is up to date. This means for
example running database migrations. 

### clean

The clean task will remove any files installed by b5. This includes for example the node_modules-directory
introduced by `npm install`.

## Assets building

### css

This task will build the CSS files necessary for your project. It will build these files once and then
exit. May use Sass or less for doing so.

### js

The js task will build any Javascript files inside your project. This may use Typescript or just webpack to
combine multiple files. It will exit after doing so.

### watch

The watch task will build CSS and Javascript files on every change. It will stay alive until canceled
using Ctrl+C. No other jobs are started, so for example no browsersync will be launched.

## Local execution

### run

Starts the local development server, most of the time we will use something like http://localhost:8000/ for
this. The development server may be started inside a docker container using docker-compose.

### halt

Stops the development server.

### shell

Execute a development shell for the project. May differ based on the project.

**Note:** Django projects will not use `b5 shell` to execute the `python manage.py shell` as `b5 shell` will
most commonly start a docker shell (like `docker-compose run --rm web /bin/bash --login`). We use `b5 django:shell`
instead. This behavior is true for other frameworks providing its own development shell, too.   

## Deployment

### deploy

Takes at least one parameter: Server to deploy to (example: `b5 deploy staging`)

Will deploy all the changes from the local repository to the server. 

### deploy:install

Like `deploy` but will only setup the project on the server. It will not try to run tasks for
updating the project as these will fail (example: running database migrations without having configured
the database connection is a bad idea).

## Mandatory tasks

The following tasks must be available in **every** project:

* install
* update

If no installation is necessary the tasks should just do nothing, but still must be available.

## Further tasks

The following tasks may exist, but are not as standardised as the tasks above:

### Database handling

* db:init - Initialize an empty DB from scratch
* db:download - Download DB from server, might strip some tables for easy usage.
* db:export - Export the local database.
* db:import - Import a database dump.
* db:prepare:dev - Prepare the database for development (changing configuration, truncate tables, …)

Database dumps are normally stored inside `$CONFIG_paths_db`, which in general is set to `_db/` inside the
project root.

### Command calling

It is most common to provide tasks to execute the tools we use inside the b5 context. This might for example
mean calling `docker-compose` with all the neccessary environment changes set. Tasks provided here might
include:

* docker-compose
* pipenv
* composer
* npm
* …

Most of the times these Tasks just use the [modules](05_modules.md) b5 provides. Example:

```bash
task:npm() {
    npm:npm "$@"
}
```

### Other

* browsersync - Start `b5 watch` + browsersync
* TODO
