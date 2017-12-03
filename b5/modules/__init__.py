MODULES = {
    'test': 'b5.modules.test.TestModule',
    'legacy': 'b5.modules.legacy.LegacyModule',
}


class BaseModule(object):
    def __init__(self, name, config, state, **kwargs):
        self.name = name
        self.config = config
        self.state = state
        self.kwargs = kwargs
        self.validate_config()

    def validate_config(self):
        pass

    def _script_function_call(self, method, args=None, kwargs=None):
        return '''
{module}:{method}() {{
    b5-execute --state-file {state_file} --module {module} --method {method} "$@"
}}
        '''.format(
            module=self.name,
            method=method,
            state_file=self.state.stored_name,
        )

    def get_script(self):
        return ''
