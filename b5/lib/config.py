import os
import yaml
from collections.abc import Mapping
from ..exceptions import B5ExecutionError
from packaging import version
from .. import VERSION as B5_VERSION


def find_configs(state, configs):
    run_path = os.path.realpath(state.run_path)
    found_configs = []
    for config in configs:
        config_path = os.path.join(run_path, os.path.expanduser(config))
        if os.path.exists(config_path):
            found_configs.append({
                'config': config,
                'path': config_path,
            })
    return found_configs


class ConfigHandler:

    def load(self, run_path, file_paths):
        full_config = {}
        for file_path in file_paths:
            loaded_config = self.load_config_file(run_path, file_path)
            full_config = ConfigHandler.merge_config(full_config, loaded_config)
        return self.validate_config(full_config)

    def load_config_file(self, run_path, file_path):
        print(os.path.expanduser(file_path))
        config_path = os.path.join(run_path, os.path.expanduser(file_path))
        print(config_path)
        if os.path.exists(config_path):
            file_handle = open(config_path, 'r')
            config = yaml.safe_load(file_handle)
            file_handle.close()
            return config
        return {}

    def validate_config(self, config):
        if 'version' in config:
            config_version = version.parse(config['version'])
            if config_version > version.parse(B5_VERSION):
                raise B5ExecutionError(
                    'config.yml requires more recent version of b5 (>=%s), aborting' % config['version'])
        return config

    @staticmethod
    def merge_config(full_config, loaded_config):
        for key, value in loaded_config.items():
            if (key in full_config and isinstance(full_config[key], dict)
                    and isinstance(loaded_config[key], Mapping)):
                full_config[key] = ConfigHandler.merge_config(full_config[key], loaded_config[key])
            else:
                full_config[key] = loaded_config[key]
        return full_config
