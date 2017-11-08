from ..modules import MODULES
from .importutils import import_string


def module_load(project_path, run_path, module_key, module_config, config):
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
        project_path=project_path,
        run_path=run_path,
        global_config=config,
    )
    return module
