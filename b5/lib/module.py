from ..exceptions import B5ExecutionError
from ..modules import MODULES, BaseModule
from .importutils import import_string
from .state import State


def load_module(state: State, module_key: str) -> BaseModule:
    if 'modules' not in state.config or module_key not in state.config['modules']:
        raise RuntimeError('Module %s is not defined in config' % module_key)
    module_config = state.config['modules'][module_key]

    module_class_key = module_key
    if not isinstance(module_config, dict):
        module_config = {}
    if 'class' in module_config:
        module_class_key = module_config['class']

    module_import_path = module_class_key
    if module_class_key in MODULES:
        module_import_path = MODULES[module_class_key]
    if '.' not in module_import_path:
        raise B5ExecutionError(
            'Module seems not to be valid (key=%s/import=%s), please check config' %
            (
                module_key, module_import_path,
            ),
        )

    try:
        module_class = import_string(module_import_path)
    except ImportError:
        raise B5ExecutionError('Module could not be imported (%s), please check config' % module_key)

    module = module_class(
        name=module_key,
        config=module_config,
        state=state,
    )
    return module
