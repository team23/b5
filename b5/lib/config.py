import yaml
import os


def load_config(run_path):
    CONFIG_FILE = os.path.join(run_path, 'config.yml')
    LOCAL_CONFIG_FILE = os.path.join(run_path, 'local.yml')

    if os.path.exists(CONFIG_FILE):
        fh = open(CONFIG_FILE, 'r')
        config = yaml.load(fh)
        if config is None:
            config = {}
    else:
        config = {}

    if os.path.exists(LOCAL_CONFIG_FILE):
        lfh = open(LOCAL_CONFIG_FILE, 'r')
        config['local'] = yaml.load(lfh)

    return config
