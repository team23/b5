import os
import shlex

from .module import module_load


def construct_script_source(project_path, run_path, config, taskfiles, command, args):
    from .. import B5_BASH_PATH

    script = ''
    script += open(os.path.join(B5_BASH_PATH, 'init.sh'), 'r').read()
    script += open(os.path.join(B5_BASH_PATH, 'functions.sh'), 'r').read()
    script += open(os.path.join(B5_BASH_PATH, 'default_tasks.sh'), 'r').read()

    script += 'PROJECT_PATH=%s\n' % shlex.quote(project_path)
    script += 'RUN_PATH=%s\n' % shlex.quote(run_path)
    script += 'TASKFILE_PATHS=(%s)\n' % ' '.join([shlex.quote(t[1]) for t in taskfiles])

    script += 'BUILD_PATH=%s\n' % shlex.quote(run_path)  # backwards compatibility
    if taskfiles:
        script += 'TASKFILE_PATH=%s\n' % shlex.quote(taskfiles[0][1])  # backwards compatibility

    if 'modules' in config:
        for module_key in config['modules']:
            module_config = config['modules'][module_key]
            module = module_load(project_path, run_path, module_key, module_config, config)
            script += module.get_script()

    script += 'cd %s\n' % shlex.quote(run_path)
    for taskfile in taskfiles:
        script += 'source %s\n' % shlex.quote(taskfile[1])

    script += 'b5:function_exists %s && b5:run %s || b5:error "Task not found" \n' % (
        shlex.quote('task:%s' % command),
        ' '.join(
            [shlex.quote('task:%s' % command)] + [shlex.quote(a) for a in args]
        )
    )

    return script
