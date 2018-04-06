"""Core creation of indexes and schema."""

import logging
import typing

from goblin.element import Edge
from goblin.element import Vertex
from goblin.element import VertexProperty
from goblin.properties import Property
from gremlin_python.process.traversal import Cardinality
import goblin.properties as properties

from .exceptions import InvalidElementError
from .exceptions import UnsupportedPropertyCardinality
from .exceptions import UnsupportedPropertyType
from .exceptions import WrongPropertyType
from .utils import get_iterable_from_module


_LOGGER = logging.getLogger(__name__)

_SUPPORTED_PROPERTY_TYPES = {
    # In most cases we could just concatenate as the naming seems to be compatible, but let keep this extensible.
    properties.String.__name__: 'String.class',
    properties.Integer.__name__: 'Integer.class',
    properties.Float.__name__: 'Float.class',
    properties.Boolean.__name__: 'Boolean.class',
    # These are supported by JanusGraph, but not supported by Goblin:
    #   Character
    #   Byte
    #   Short
    #   Long
    #   Double
    #   Date
    #   Geoshape
    #   UUID
}


def _get_property_type(property_instance: typing.Union[VertexProperty, Property]):
    type_str = _SUPPORTED_PROPERTY_TYPES.get(property_instance.data_type.__class__.__name__)
    if type_str is None:
        raise UnsupportedPropertyType(f"Property type {type(property_instance.data_type)} is "
                                      f"not supported by Goblinoid")

    return type_str


def _get_property_cardinality(property_instance: Cardinality) -> str:
    """Convert Goblin's cardinality enum to its representation in Gremlin's groovy shell."""
    if property_instance.cardinality == Cardinality.single:
        return 'Cardinality.SINGLE'
    elif property_instance.cardinality == Cardinality.set_:
        return 'Cardinality.SET'
    elif property_instance.cardinality == Cardinality.list_:
        return 'Cardinality.LIST'
    else:
        raise UnsupportedPropertyCardinality(f"Cardinality type {type(property_instance.cardinality)} is not supported")


def create_schema(module_import: str, models_iterable: str, output_file: str) -> None:
    iterable = get_iterable_from_module(module_import, models_iterable)

    with open(output_file, 'w') as output:
        output.write("mgmt = graph.openManagement()\n\n")

        for model_class in iterable:
            output.write(f"//\n// {model_class.__name__}\n//\n")

            if issubclass(model_class, Vertex):
                output.write(f"mgmt.makeVertexLabel('{model_class.__label__}').make()\n\n")
            elif issubclass(model_class, Edge):
                output.write(f"mgmt.makeEdgeLabel('{model_class.__label__}).make()\n\n")
            else:
                raise InvalidElementError(f"Element {model_class.__name__} from {module_import} present in "
                                          f"iterable {models_iterable} is not of type "
                                          f"goblin.element.Edge nor goblin.element.Vertex")

            for property_name, property_instance in model_class.__properties__.items():
                if not isinstance(property_instance, (Property, VertexProperty)):
                    _LOGGER.warning(f"Skipping property {property_name!r}, not of type Property nor VertexProperty")
                    continue

                db_name = property_instance.getdb_name() or property_name
                property_type = _get_property_type(property_instance)

                # TODO: check that we are not using Property on Vertexes but rather VertexProperty
                if isinstance(property_instance, VertexProperty):
                    if not issubclass(model_class, Vertex):
                        raise WrongPropertyType(f"Property {property_name!r} in {model_class} is of "
                                                f"type {type(property_instance)}, but should be Property.")

                    property_cardinality = _get_property_cardinality(property_instance)
                    output.write(f"mgmt.makePropertyKey('{db_name}')"
                                 f".dataType({property_type})"
                                 f".cardinality({property_cardinality}).make()")
                else:
                    if not issubclass(model_class, Edge):
                        raise WrongPropertyType(f"Property {property_name!r} in {model_class} is of "
                                                f"type {type(property_instance)}, but should be VertexProperty.")

                    output.write(f"mgmt.makePropertyKey('{db_name}')"
                                 f".dataType({property_type}).make()")

                if db_name != property_name:
                    output.write(f"  // {model_class.__name__}.{property_name}")

                output.write('\n')

            output.write('\n')

        output.write("mgmt.commit()\n")


def create_indexes(module_import: str, models_iterable: str, output_file: str):
    pass
    # TODO: implement
    # iterable = get_iterable_from_module(module_import, models_iterable)
