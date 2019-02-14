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

"""Exception hierarchy definition."""


class GoblinoidExceptionBase(Exception):
    """"A base class for Goblinoid exception hierarchy."""


class ModuleImportError(GoblinoidExceptionBase):
    """An exception raised on module import failure."""


class ModelsIterableError(GoblinoidExceptionBase):
    """An exception raised when models iterable is not found."""


class InvalidElementError(GoblinoidExceptionBase):
    """An exception raised when there is found invalid element in the registered element iterable."""


class UnsupportedPropertyType(GoblinoidExceptionBase):
    """Raised on unsupported property type."""


class UnsupportedPropertyCardinality(GoblinoidExceptionBase):
    """Raised on unsupported cardinality type."""


class WrongPropertyType(GoblinoidExceptionBase):
    """Raised when wrong property type is used for an element."""


class PropertyNameClashError(GoblinoidExceptionBase):
    """Raised if a same property name is used for edge and vertex at the same time."""


class MultipleLabelsError(GoblinoidExceptionBase):
    """Raised if multiple labels with a same name found."""
