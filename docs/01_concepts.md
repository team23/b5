# Core concepts

We use a file called `Taskfile` for defining all our tasks. The Taskfile will include all the tasks you
may later call and is the central entry point for task calling. The Taskfile itself is based on bash
scripting, so has a lean and easy to read syntax. The basic idea is simple:  
A function defined in the Taskfile using the schema `task:{name}` may be called by b5 using `b5 {name}`.

So, the Taskfile will include all tasks for your project. It is common to use external tools (hey, as I said
before: bash scripting) for task fulfilment. So a `css` task may for example call gulp for doing the heavy
lifting. b5 itself is _not_ intended to provide business ready methods for all project jobs. Instead it
is by design intended to allowing users to use any external tools that fit for these jobs perfectly. Each
task can use a different tool (gulp, fabric, grunt, …) for fulfilment. This also ensures we can easily
replace the tools we use while still calling the same commands for every project. `b5 css` may call grunt
for some projects and gulp for others, but each developer has only to know about `b5 css`.

b5 will load the Taskfile by looking into your project root folder (the directory `.git` lives in) and then tries
to find `build/Taskfile` from this entry point. It will then load the Taskfile (using bash `source`) and
just call it with the parameters it was called with itself. If no parameter was passed to b5 it will use
the default task called "help" (which means it calls the bash function `task:help`). This task is provided
by b5 itself and will list all available tasks.

## Background

See https://hackernoon.com/introducing-the-taskfile-5ddfe7ed83bd for details about the idea of the Taskfile.
Please note, that we use some different concepts, so use the documentation provided here.

## Tools

In general we will use gulp for local building of assets (CSS, JS, sprites, …) and fabric for deployment jobs
(based on fabdeploit). Additional tools to use may be mysqldump for database dump, rsync for downloading
media files, etc.
