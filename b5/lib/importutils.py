from importlib import import_module
from types import ModuleType


def import_string(dotted_path: str) -> ModuleType:
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImportError("%s doesn't look like a module path" % dotted_path)

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class' % (
                module_path, class_name,
            ),
        )
