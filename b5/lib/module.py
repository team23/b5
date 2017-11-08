from ..modules import MODULES
from .importutils import import_string


class BaseModule(object):
    def __init__(self, name, config, global_config, **kwargs):
        self.name = name
        self.config = config
        self.global_config = global_config
        self.kwargs = kwargs
        self.validate_config()

    def validate_config(self):
        pass

    def get_script(self):
        raise NotImplementedError('Subsclass must provide this')


def module_load(module_key, module_config, config):
    module_class_key = module_key
    if isinstance(module_config, dict) and 'class' in module_config:
        module_class_key = module_config['class']
    if not module_class_key in MODULES:
        raise RuntimeError('Module not found (%s)' % module_key)

    try:
        module_class = import_string(MODULES[module_class_key])
    except ImportError:
        raise RuntimeError('Module could not be imported (%s)' % module_key)

    module = module_class(
        name=module_key,
        config=module_config,
        global_config=config,
    )
    return module
