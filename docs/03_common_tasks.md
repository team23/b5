# Tasks we use

The following tasks are required to work as described below for every project and should be available if
necessary.


## Project setup

### install

Side note: `install` has formerly be known as `setup`.

The install task will setup the project for you. It will install dependencies (npm, virtualenv, …), and
make sure an initial config exists.

You may need to update `local.yml` after initially running this tasks and then run `b5 update` to recreate
the config provided.

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

Starts the local development server, most of the time we will use http://localhost:8000 for this. The
development server may be started inside a docker container using docker-compose.

### halt

Stops the development server.

### shell

Execute a development shell for the project. May differ based on the project.

**Note:** Django projects will not use `b5 shell` to execute the `python manage.py shell` as `b5 shell` will
most commonly start a docker shell (`docker-compose run --rm web /bin/bash --login`). We use `b5 django_shell`
instead. This behavior is true for other frameworks providing its own development shell, too.   

## Deployment

### deploy

Takes one parameter: Server to deploy to (example: `b5 deploy staging`)

Will deploy all the changes from the local repository to the server. 

### deploy_install

Like `deploy` but will only setup the project on the server. It will not try to run tasks for
updating the project as these will fail (example: running database migrations without having configured
the database connection is a bad idea).

## Further tasks

TODO!

* docker
* import_production_db
* dbdump
* dbimport
* browsersync


## Mandatory tasks

The following tasks must be available in **every** project:

* install
* update

If no installation is necessary the tasks should just do nothing, but still must be available.