from packaging import version

from .. import VERSION
from ..exceptions import B5ExecutionError

B5_VERSION = version.parse(VERSION)


def ensure_config_version(config_version_str: str) -> None:
    if not isinstance(config_version_str, str):
        config_version_str = str(config_version_str)
    try:
        config_version = version.parse(config_version_str)
    except TypeError as O_o:
        raise B5ExecutionError(f'Version in config.yml ({config_version_str}) could not be parsed') from O_o
    if config_version > B5_VERSION:
        raise B5ExecutionError(
            f'config.yml requires more recent version of b5 (>={config_version_str}), aborting',
        )
