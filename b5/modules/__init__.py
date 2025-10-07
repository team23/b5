import re
from typing import Any, ClassVar, Optional

from ..lib.config import merge_config
from ..lib.state import State

CONFIG_PREFIX_RE = re.compile('[^A-Z0-9]')
MODULES: dict[str, str] = {
    'test': 'b5.modules.test.TestModule',
    'virtualenv': 'b5.modules.virtualenv.VirtualenvModule',
    'pipenv': 'b5.modules.pipenv.PipenvModule',
    'npm': 'b5.modules.npm.NpmModule',
    'composer': 'b5.modules.composer.ComposerModule',
    'docker': 'b5.modules.docker.DockerModule',
    'template': 'b5.modules.template.TemplateModule',
    'comlipy': 'b5.modules.comlipy.ComlipyModule',
}


class BaseModule:
    DEFAULT_CONFIG: ClassVar = {}

    def __init__(
            self,
            name: str,
            config: dict[str, Any],
            state: State,
            **kwargs: Any,
    ) -> None:
        self.name = name
        self.config = merge_config(self.DEFAULT_CONFIG, config)
        self.state = state
        self.kwargs = kwargs
        self.validate_config()
        self.prepare_config()

    def validate_config(self) -> None:
        pass

    def prepare_config(self) -> None:
        pass

    def _script_config_vars(self) -> str:
        from ..lib.script import config_script_source

        return config_script_source(self.config, prefix=CONFIG_PREFIX_RE.sub('_', self.name.upper()))

    def _script_function_call(
            self,
            external_method: str,
            method: str | None = None,
    ) -> str:
        return '''
{module}:{external_method}() {{
    b5-execute --state-file {state_file} --module {module} --method {method} --args "$@"
}}
        '''.format(
            module=self.name,
            external_method=external_method,
            state_file=self.state.stored_name,
            method=method if method else f'execute_{external_method}',
        )

    def _script_function_source(
            self,
            external_method: str,
            source: str,
    ) -> str:
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
        return f'''
{self.name}:{external_method}() {{
    {self.is_installed_script()}
    {source}
}}
        '''

    def get_script(self) -> str:
        return ''

    def create_is_installed_script(
            self,
            module: str | None = None,
            module_bin: str | None = None,
    ) -> str:
        """
        Generate an is_installed_script using the passed parameters.

        Args:
            module: the name of the module or self.name if is `None`
            module_bin: the modules binary or `module` if is `None`

        Returns: str
        """
        module = module if module else self.name
        module_bin = module_bin if module_bin else module

        return f'''
                    if ! b5:bin_exists "{module_bin}"; then
                        b5:error "'{module}' (bin: '{module_bin}') seems not to be installed!";
                    fi
                '''

    def is_installed_script(self) -> str:
        """
        Can be overridden by child classes in order to run a check to determine whether the local bin is
        available or not. This can be done manually or by using the `create_is_installed_script` method
        which already provides all necessary logic.

        Returns: str
        """
        return ''
