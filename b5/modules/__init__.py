from ..lib.config import merge_config
import re


CONFIG_PREFIX_RE = re.compile('[^A-Z0-9]')
MODULES = {
    'test': 'b5.modules.test.TestModule',
    'legacy': 'b5.modules.legacy.LegacyModule',
    'virtualenv': 'b5.modules.virtualenv.VirtualenvModule',
    'npm': 'b5.modules.npm.NpmModule',
    'composer': 'b5.modules.composer.ComposerModule',
    'docker': 'b5.modules.docker.DockerModule',
    'template': 'b5.modules.template.TemplateModule',
    'laravel': 'b5.modules.laravel.LaravelModule',
}


class BaseModule(object):
    DEFAULT_CONFIG = {}

    def __init__(self, name, config, state, **kwargs):
        self.name = name
        self.config = merge_config(self.DEFAULT_CONFIG, config)
        self.state = state
        self.kwargs = kwargs
        self.validate_config()
        self.prepare_config()

    def validate_config(self):
        pass

    def prepare_config(self):
        pass

    def _script_config_vars(self):
        from ..lib.script import config_script_source

        return config_script_source(self.config, prefix=CONFIG_PREFIX_RE.sub('_', self.name.upper()))

    def _script_function_call(self, external_method, method=None):
        return '''
{module}:{external_method}() {{
    b5-execute --state-file {state_file} --module {module} --method {method} --args "$@"
}}
        '''.format(
            module=self.name,
            external_method=external_method,
            state_file=self.state.stored_name,
            method=method if method else 'execute_%s' % external_method,
        )

    def _script_function_source(self, external_method, source):
        return '''
{module}:{external_method}() {{
    {source}
}}
        '''.format(
            module=self.name,
            external_method=external_method,
            source=source,
        )

    def get_script(self):
        return ''
