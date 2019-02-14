"""Various utility functions used across Goblinoid sources."""

import importlib
import typing

from .exceptions import ModuleImportError
from .exceptions import ModelsIterableError


def get_iterable_from_module(module_import: str, obj: str) -> typing.Iterable:
    """Get an item (attribute, object) from a module."""
    try:
        module = importlib.import_module(module_import)
    except Exception as exc:
        raise ModuleImportError(
            f"Failed to import module {module_import}: {str(exc)}"
        ) from exc

    try:
        result = getattr(module, obj)
    except Exception as exc:
        raise ModelsIterableError(
            f"Failed to get iterable {obj} from module {module_import}: {str(exc)}"
        ) from exc

    if not isinstance(result, typing.Iterable):
        raise ModelsIterableError(
            f"Requested object {obj} from module {module_import} "
            f"is not iterable but {type(obj)}"
        )

    return result
