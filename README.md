# b5 Task Runner

b5 is the central task runner for all projects of our agency. It tries so be as simple as possible while
empowering you to write your own tasks, extend existing ones and use b5 for all of the everyday project
jobs.

## Quick start

### Installing b5

#### Mac OS X

```bash
brew tap team23/b5 git@git.team23.de:build/homebrew-b5.git
brew install b5
```

#### Manual installation

```bash
cd installation/path/
git clone git@git.team23.de:build/b5.git
cd b5
pip install -U -r requirements.txt
pip install .
```

#### Dev installation

```bash
cd installation/path/
git clone git@git.team23.de:build/b5.git
cd b5
virtualenv --python=python3 ENV  
source ENV/bin/activate  
pip install -e . 
```

### Starting your project

**NOT READY YET:** This task is currently missing from the python implementation.

```bash
b5 init example
cd example
```

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

Now you can use `b5 make_it_happen` and your code inside the function will run. As this code is a simple
bash script you may use your normal command line tools. Feel free to use gulp, grunt, fabric, … for more
complex task excution - and call these using your Taskfile.

## Basic usage

`b5 taskname` will look for the Taskfile found under build/ in your project root. It will then execute
the function named `task:taskname` inside the Taskfile. This means you may call `b5 install` to have the
function `task:install` run.

You may add a file called Taskfile.local (`build/Taskfile.local`) for all your personal tasks. Make sure
to never add this file to git. Please be sure to add this file to your .gitignore. Otherwise you might
interfere with the local Taskfile of your colleges.

## Going further

Now you set up a simple example project including an example Taskfile. The Taskfile is the central part of
the b5 task runner which will include the calls to all of the provided tasks. Most of the tasks will
call external tools like, gulp or fabric. This is the intended behavior.

See [core concepts](docs/01_concepts.md) for some more details about the b5 concepts.

See [Taskfile format](docs/02_Taskfile_format.md) for more details on how to write your Taskfile.

See [common tasks](docs/03_common_tasks.md) for information about which tasks your Taskfile needs
to provide and what these tasks should do.

See [Configuration](docs/04_config.md) for about how to add configuration to the build process and how
to handle local configuration.

See [modules](docs/05_modules.md) for looking further into modules b5 already provides for a healthy
project setup.

See [templates](docs/06_templates.md) for more information about how to `b5 init` a project.

