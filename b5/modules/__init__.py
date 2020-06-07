import re
import shutil

from packaging import version

from b5.exceptions import B5ExecutionError
from ..lib.config import merge_config

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
        self.validate()

    def get_version(self):
        """
        Get the modules version number as str.

        Every module should implement this method itself. This is necessary, because there is no common result format
        when calling the version of a shell bin.

        Returns:
            bool
        """
        pass

    def validate(self):
        """
        Validate the module before allowing it to run.

        This way we can make sure the local installation is present and the version matches the requirements defined
        in the config.yml

        Returns:
            bool
        """
        if not self.is_installed():
            raise B5ExecutionError('Module {!r} does not seem to be installed'.format(self.name))

        if not self.is_version_matched():
            raise B5ExecutionError(
                    'Module {!r} requires at least version {!r}, installed: {!r}'.format(
                            self.name, self.config['version'], self.__get_installed_version()
                    )
            )

    def is_installed(self):
        """
        Check whether the local modules binary has been installed or not, by calling `which` on the module name.

        Returns:
            bool
        """
        return shutil.which(self.name) is not None

    def is_version_matched(self):
        """
        Check whether the local modules binary version matches the version of the config (if defined).

        The version will be ignored if `version` has not been set in the modules config, or if the module itself
        does not implement the get_version method.

        Returns:
            bool if version is <= the version defined in config; True if no version is defined in config or module.
        """
        min_version = self.config['version'] if 'version' in self.config else None

        if min_version is None or self.__get_installed_version() is None:
            return True

        return version.parse(min_version) <= version.parse(self.__get_installed_version())

    def __get_installed_version(self):
        """
        Get the currently installed version

        Returns:
            str: the str version of the current locally install module binary
        """
        if not hasattr(self, '_installed_version'):
            self._installed_version = self.get_version()

        return self._installed_version

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
