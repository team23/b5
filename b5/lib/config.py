import os
from typing import Any, Dict, List

import yaml

from ..exceptions import B5ExecutionError
from .state import State
from .version import ensure_config_version


def find_configs(
        state: State,
        configs: List[str],
) -> List[Dict[str, str]]:
    run_path = os.path.realpath(state.run_path)
    found_configs = []
    for config in configs:
        config_path = os.path.join(run_path, os.path.expanduser(config))
        if os.path.exists(config_path):
            found_configs.append({
                'config': config,
                'path': config_path,
            })
    # if not found_configs:
    #     raise B5ExecutionError('No config found, tried %s inside %s' % (', '.join(configs), run_path))
    return found_configs


def merge_config(
        cur_config: Dict[str, Any],
        new_config: Dict[str, Any],
) -> Dict[str, Any]:
    result_config = cur_config.copy()
    for key, value in new_config.items():
        if isinstance(value, dict):
            cur_value = cur_config.get(key, {})
            if isinstance(cur_value, dict):
                result_config[key] = merge_config(cur_value, value)
            else:
                result_config[key] = value
        elif isinstance(value, list):
            result_config[key] = value
        elif isinstance(value, (str, bytes, bool, int, float)):
            result_config[key] = value
        elif value is None:
            result_config[key] = value
        else:
            raise B5ExecutionError('Unknown type for config export %s' % type(value))
    return result_config


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    if 'version' in config:
        ensure_config_version(config['version'])
    return config


def load_config(state: State) -> Dict[str, Any]:
    configfiles = state.configfiles
    config = {}
    for configfile in configfiles:
        file_handle = open(configfile['path'], 'r')
        file_config = yaml.safe_load(file_handle)
        if not isinstance(file_config, dict):
            file_config = {}
        config = merge_config(config, file_config)

    validate_config(config)
    return config
