#!/usr/bin/env python3
# goblinoid
# Copyright(C) 2018-2019 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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
