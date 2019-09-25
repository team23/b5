# Project initialization

Project skeletons are provided for initial project setup using `b5-init`. By default b5 will initialize new projects
using a "basic" template which only provides a basic project layout. See https://git.team23.de/build/b5-skel-basic
for details about the basic skeleton.

## Usage

```console
$ b5-init TEST-PROJECT
Cloning into '/Users/ddanier/TEST-PROJECT'...
remote: Counting objects: 16, done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 16 (delta 2), reused 0 (delta 0)
Unpacking objects: 100% (16/16), done.
Initialized empty Git repository in /Users/ddanier/TEST-PROJECT/.git/
Have a good project time.
Successful initialized TEST-PROJECT
  skeleton used: https://git.team23.de/build/b5-skel-basic.git
  project path: /Users/ddanier/TEST-PROJECT

$ cd TEST-PROJECT

$ ls -lh
total 16
-rw-r--r--  1 ddanier  staff   898B  1 Jun 22:28 DEPLOY.md
-rw-r--r--  1 ddanier  staff   419B  1 Jun 22:28 README.md
drwxr-xr-x  4 ddanier  staff   128B  1 Jun 22:28 build
drwxr-xr-x  3 ddanier  staff    96B  1 Jun 22:28 web

$ tree
.
├── DEPLOY.md
├── README.md
├── build
│   ├── Taskfile
│   └── config.yml
└── web
    └── index.html

2 directories, 5 files

$ cat build/Taskfile
#!/usr/bin/env bash
# b5 Taskfile, see https://git.team23.de/build/b5 for details

# Basic housekeeping tasks
task:install() {
    # Use modules to install all project dependencies
    # virtualenv:install
    true
}

task:update() {
    # Use modules to keep dependencies updated and run maintainence tasks (for example: DB migrations)
    # virtualenv:update
    true
}

# Fabric example, for deployment
# ------------------------------

## Run fabric from b5, so it is accessible from every path inside the project
#task:fab() {
#    virtualenv:run fab "$@"
#}
#
## Run fabric based deployment
#task:deploy() {
#    if [ -z "${1:-}" ]
#    then
#        echo "Usage: b5 deploy <servername> [options]"
#        echo ""
#        b5:abort "Argument missing: server name"
#    fi
#    virtualenv:run fab "$1" deploy:"${2:-}"
#}

$ b5 install
b5 0.12.0
Found project path (/Users/ddanier/TEST-PROJECT)
Found Taskfile (~/.b5/Taskfile, Taskfile)
Executing task install

Task exited ok
```

## Current skeletons

### basic

Basic project template, only providing an minimal set of files.

See: https://git.team23.de/build/b5-skel-basic

### django

Basic django project template. The skeleton will ask you about which versions (Django, Python) and database
you want to use. Please make sure the parameters you use are valid.

See: https://git.team23.de/build/b5-skel-django

## magento 2

Basic Magento 2 project template.

See: https://git.team23.de/build/b5-skel-magento2

## Providing your own skeleton

A b5 skeleton is just a normal git repository. You may use any valid git URL for initializing your new project,
if only providing a name b5 will try to clone "https://git.team23.de/build/b5-skel-$NAME.git" by default.

After cloning the git repository b5 will then remove the .git/ path from it and use `git init` to create a new
repository. You may provide additional initialization by providing an init/ path inside the repository. b5 will
use this path as its run_path and then execute the "project:init"-task of the Taskfile inside init/ (so init/Taskfile
will be used - you may provide init/config.yml as well). After this init task is run b5 will completely remove
init/ from the newly created project.

See https://git.team23.de/build/b5-skel-basic/blob/master/init/ and
https://git.team23.de/build/b5-skel-basic/blob/master/init/Taskfile for a really minimal example of this mechanism.

**Important:** The skeleton init should provide a project directory in a state like developers would have after
cloning the project the first time. This means it's totally ok to run `b5 install` and `b5 update` afterwards.

