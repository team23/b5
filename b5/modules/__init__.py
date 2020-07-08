import re

from b5.lib.config import merge_config

CONFIG_PREFIX_RE = re.compile('[^A-Z0-9]')
MODULES = {
    'test': 'b5.modules.test.TestModule',
    'legacy': 'b5.modules.legacy.LegacyModule',
    'virtualenv': 'b5.modules.virtualenv.VirtualenvModule',
    'pipenv': 'b5.modules.pipenv.PipenvModule',
    'npm': 'b5.modules.npm.NpmModule',
    'composer': 'b5.modules.composer.ComposerModule',
    'docker': 'b5.modules.docker.DockerModule',
    'template': 'b5.modules.template.TemplateModule',
}


class BaseModule:
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
        from b5.lib.script import config_script_source

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
        """
        Create a shell function script for a b5 module.
        This also prepends the return value of `is_installed_script` for (optional) evaluation whether the given
        module exists or not. (Therefore `is_installed_script` must be implemented in the module class).

        Args:
            external_method: the name of the external method that should be executed and has been wrapped
                by the b5 module.
            source: the shell code that should be executed whenever the method will be triggered

        Returns: str
        """
        return '''
{module}:{external_method}() {{
    {installed_script}
    {source}
}}
        '''.format(
            module=self.name,
            external_method=external_method,
            source=source,
            installed_script=self.is_installed_script()
        )

    def get_script(self):
        return ''

    def create_is_installed_script(self, module=None, module_bin=None):
        """
        Generate an is_installed_script using the passed parameters.

        Args:
            module: the name of the module or self.name if is `None`
            module_bin: the modules binary or `module` if is `None`

        Returns: str
        """
        module = module if module else self.name

        return '''
                    if ! b5:bin_exists "{module_bin}"; then 
                        b5:error "'{module}' (bin: '{module_bin}') seems not to be installed!"; 
                    fi
                '''.format(
                module=module if module else self.name,
                module_bin=module_bin if module_bin else module,
        )

    def is_installed_script(self):
        """
        Can be overridden by child classes in order to run a check to determine whether the local bin is
        available or not. This can be done manually or by using the `create_is_installed_script` method
        which already provides all necessary logic.

        Returns: str
        """
        return ''
