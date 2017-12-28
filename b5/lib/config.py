import yaml
import os

from ..exceptions import B5ExecutionError


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
    #if not found_configs:
    #    raise B5ExecutionError('No config found, tried %s inside %s' % (', '.join(configs), run_path))
    return found_configs


def merge_config(cur_config, new_config):
    result_config = cur_config.copy()
    for key, value in new_config.items():
        if isinstance(value, dict):
            result_config[key] = merge_config(cur_config.get(key, {}), value)
        elif isinstance(value, list):
            result_config[key] = value
        elif isinstance(value, (str, bytes, int, float)):
            result_config[key] = value
        elif value is None:
            result_config[key] = value
        else:
            raise RuntimeError('Unknown type for config export %s' % type(value))
    return result_config


def load_config(state):
    configfiles = state.configfiles
    config = {}
    for configfile in configfiles:
        fh = open(configfile['path'], 'r')
        file_config = yaml.load(fh)
        if file_config is None:
            file_config = {}
        config = merge_config(config, file_config)

    return config

