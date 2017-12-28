# Templates

**NOT READY YET:** This is currently missing from the python implementation.

Templates are provided for initial project setup using `b5 init`. By default b5 will initialize new projects
using a "minimal" template which only provides a basic layout.

## Usage

```console
$ b5 init TEST-PROJECT
b5 0.6.0
PROJECT_PATH could not be found. I looked for a .git directory in all parent paths.
(Only default tasks are available)
Executing task 'init'

Initialized empty Git repository in /Users/ddanier/TEST-PROJECT/.git/
All set up. You may now start using TEST-PROJECT

Task exited ok

$ cd TEST-PROJECT

$ ls -lh
total 0
drwxr-xr-x  4 ddanier  staff   128B 27 Sep 23:16 build
drwxr-xr-x  3 ddanier  staff    96B 27 Sep 23:16 web

$ cat build/Taskfile
#!/usr/bin/env bash
# b5 Taskfile, see https://git.team23.de/build/b5 for details

task:example() {
    echo "This is a minimal example task"
    echo ""
    echo "Just start writing all commands you need into simple bash function"
    echo "You may use parameters like \$1 (\$1=$1), too"
}

$ b5 example
b5 0.6.0
Found PROJECT_PATH (/Users/ddanier/TEST-PROJECT)
Found Taskfile (/Users/ddanier/TEST-PROJECT/build/Taskfile)
Executing task 'example'

This is a minimal example task

Just start writing all commands you need into simple bash function
You may use parameters like $1 ($1=), too

Task exited ok
```

## Current templates

### minimal

Minimal example project.

### typo3-test

Test setup for TYPO3, not intended for production use. Installs TYPO3 using composer.
