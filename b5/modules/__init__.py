from ..lib.config import merge_config

MODULES = {
    'test': 'b5.modules.test.TestModule',
    'legacy': 'b5.modules.legacy.LegacyModule',
    'virtualenv': 'b5.modules.virtualenv.VirtualenvModule',
}


class BaseModule(object):
    DEFAULT_CONFIG = {}

    def __init__(self, name, config, state, **kwargs):
        self.name = name
        self.config = merge_config(self.DEFAULT_CONFIG, config)
        self.state = state
        self.kwargs = kwargs
        self.validate_config()

    def validate_config(self):
        pass

    def _script_function_call(self, external_method, method=None):
        return '''
{module}:{external_method}() {{
    b5-execute --state-file {state_file} --module {module} --method {method} "$@"
}}
        '''.format(
            module=self.name,
            external_method=external_method,
            state_file=self.state.stored_name,
            method=method if method else 'execute_%s' % external_method,
        )

    def _script_function_script(self, external_method, script):
        return '''
{module}:{external_method}() {{
    {script}
}}
        '''.format(
            module=self.name,
            external_method=external_method,
            script=script,
        )

    def get_script(self):
        return ''
