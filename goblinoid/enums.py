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
