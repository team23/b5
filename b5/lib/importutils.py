from importlib import import_module
from types import ModuleType


def import_string(dotted_path: str) -> ModuleType:
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as e:
        raise ImportError(f"{dotted_path} doesn't look like a module path") from e

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as e:
        raise ImportError(
            f'Module "{module_path}" does not define a "{class_name}" attribute/class',
        ) from e
