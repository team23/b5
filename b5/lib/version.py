from packaging import version

from .. import VERSION
from ..exceptions import B5ExecutionError

B5_VERSION = version.parse(VERSION)


def ensure_config_version(config_version_str):
    config_version = version.parse(config_version_str)
    if config_version > B5_VERSION:
        raise B5ExecutionError('config.yml requires more recent version of b5 (>=%s), aborting' % config_version_str)
