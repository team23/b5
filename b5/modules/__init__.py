MODULES = {
    'test': 'b5.modules.test.TestModule',
}


class BaseModule(object):
    def __init__(self, name, config, project_path, run_path, global_config, **kwargs):
        self.name = name
        self.config = config
        self.project_path = project_path
        self.run_path = run_path
        self.global_config = global_config
        self.kwargs = kwargs
        self.validate_config()

    def validate_config(self):
        pass

    def _script_function_call(self, method, args=None, kwargs=None):
        return '''
{module}:{method}() {{
    b5e --project-path {project_path} --run-path {run_path} --module {module} --method {method} "$@"
}}
        '''.format(
            module=self.name,
            method=method,
            project_path=self.project_path,
            run_path=self.run_path,
        )

    def get_script(self):
        return ''
