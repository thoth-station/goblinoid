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
