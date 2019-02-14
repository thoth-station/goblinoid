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

"""Definition of possible values for decorators.

Please refer to official documentation for explanation - http://docs.janusgraph.org/0.2.0/schema.html
"""

from enum import auto
from enum import Enum


class EdgeMultiplicity(Enum):
    """Edge multiplicity settings."""

    MULTI = auto()
    SIMPLE = auto()
    MANY2ONE = auto()
    ONE2MANY = auto()
    ONE2ONE = auto()


class PropertyDataType(Enum):
    """Property data types."""

    STRING = auto()
    CHARACTER = auto()
    BOOLEAN = auto()
    BYTE = auto()
    SHORT = auto()
    INTEGER = auto()
    LONG = auto()
    FLOAT = auto()
    DOUBLE = auto()
    DATE = auto()
    GEOSHAPE = auto()
    UUID = auto()
