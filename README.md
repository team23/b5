![b5 ready](assets/badges/b5_ready.png)

# b5 Task Runner

b5 is the central task runner for all projects of our agency (TEAM23 - www.team23.de). It tries to be as simple
as possible while empowering you to write your own tasks, extend existing ones and use b5 for all of the everyday
project jobs.

## Basic usage and concept

`b5 {taskname}` will look for a file called [`Taskfile`](docs/02_Taskfile_format.md) found under build/ in your project
root. It will then execute the function named `task:{taskname}` inside the Taskfile (which is a normal bash script).
This means you may call `b5 install` to have the function `task:install` run.

The basic idea of b5 is to allow you to easily put your daily shell jobs into the Taskfile and provide a
common schema for running these tasks. So `b5 css` for example will always build the CSS files for your
project regardless of the CSS preprocessor used in this particular project (could be: less, sass, …). As b5
uses bash scripting as the Taskfile format it is easy to understand and enhance.

b5 in addition provides some modules to ease the usage of some common tools used in web development (like
[npm](docs/modules/npm.md), [composer](docs/modules/composer.md), [pipenv](docs/modules/pipenv.md),
[docker](docs/modules/docker.md), …). In addition it defines some
[common task names](docs/03_common_tasks.md) to introduce a good convention for your task naming schema. This
will allow new developers to get on board faster - not need to care too much about the
project setup itself.

You may pass parameters to your tasks like `b5 some_task some_parameter` and use normal bash parameter handling
to use these parameters (`$1`, or better `${1}`). Please note that b5 will abort when accessing a non existent
parameter, use bash default values when necessary (`${1:-default}`).

**Hint:** You may add a file called Taskfile.local (`build/Taskfile.local`) for all your personal tasks. Make
sure to never add this file to git. Please be sure to add this file to your .gitignore. Otherwise you might
interfere with the local Taskfile of your colleges.

## Quick start

Install b5 using `pipx install b5` or `pip install b5` (For Mac OS X you may use `brew install b5` after
adding our tap). See [detailed installation instructions](docs/00_install.md).

**Note for my TEAM23 colleagues:** Please make sure to install the
[additional dependencies](docs/00_install.md#additional-dependencies).

### Starting your project

```bash
b5-init example-project
cd example-project
# start working on the new project
```

**Note:** You may use `b5-init -s $SKELETON example` to initialize the project using an skeleton. By default
b5 will use the "basic" skeleton. See [project initialization](docs/06_project_init.md) for more details.

### Defining your tasks (build/Taskfile)

b5 initialized your project with an example Taskfile (see `build/Taskfile`). For adding new tasks just
write bash functions prefixed with `task:`, like:

```bash
#!/usr/bin/env bash
# b5 Taskfile, see https://git.team23.de/build/b5 for details

task:make_it_happen() {
    echo "Yeah, it happened"
}
```

### Running your tasks

Now you can use `b5 make_it_happen` and your code inside the function will run. As this code is a simple
bash script you may use your normal command line tools. Feel free to use gulp, grunt, fabric, … for more
complex task excution - and call these using your Taskfile.

**Note:** The Taskfile is always executed inside the "run-path", which defaults to `build/`. Make
sure to switch path, when neccessary. I recommend using a subshell (see
["( … )" subshell syntax](http://www.gnu.org/software/bash/manual/html_node/Command-Grouping.html)) when
doing so.

## Going further

Now you set up a simple example project including an example Taskfile. The Taskfile is the central part of
the b5 task runner which will include the calls to all of the provided tasks. Most of the tasks will
call external tools like, gulp or fabric. This is the intended behavior.

See [detailed installation instruction](docs/00_install.md) for some more details the installation of b5.

See [core concepts](docs/01_concepts.md) for some more details about the b5 concepts.

See [Taskfile format](docs/02_Taskfile_format.md) for more details on how to write your Taskfile.

See [common tasks](docs/03_common_tasks.md) for information about which tasks your Taskfile needs
to provide and what these tasks should do.

See [Configuration](docs/04_config.md) for about how to add configuration to the build process and how
to handle local configuration.

See [modules](docs/05_modules.md) for looking further into modules b5 already provides for a healthy
project setup.

See [project initialization](docs/06_project_init.md) for more information about how to `b5-init` a project.

## b5 logo

You may use the b5 logo when referring to b5:  
![b5 Logo](assets/logo_small.png)  
(see [assets/](assets/) for other formats)

Also feel free to add a b5 badge to your project after you made it "b5 ready":  
![b5 ready](assets/badges/b5_ready.png)  
(see [assets/badges/](assets/badges/) for other formats)
