"""Core creation of indexes and schema."""

import logging
import typing

from goblin.element import Edge
from goblin.element import Vertex
from goblin.element import VertexProperty
from goblin.properties import Property
from gremlin_python.process.traversal import Cardinality
import goblin.properties

from .exceptions import InvalidElementError
from .exceptions import UnsupportedPropertyCardinality
from .exceptions import MultipleLabelsError
from .exceptions import UnsupportedPropertyType
from .exceptions import PropertyNameClashError
from .exceptions import WrongPropertyType
from .utils import get_iterable_from_module


_LOGGER = logging.getLogger(__name__)

_SUPPORTED_PROPERTY_TYPES = {
    # In most cases we could just concatenate as the naming seems to be compatible, but let keep this extensible.
    goblin.properties.String.__name__: 'String.class',
    goblin.properties.Integer.__name__: 'Integer.class',
    goblin.properties.Float.__name__: 'Float.class',
    goblin.properties.Boolean.__name__: 'Boolean.class',
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


def _get_property_type(property_instance: typing.Union[VertexProperty, Property]) -> str:
    """Get type of property based on classes defined in Goblin."""
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


def create_schema(module_import: str, models_iterable: str, output_file: str,
                  remove_schema_maker: bool=True, schema_vertex_identifier: str=None) -> None:
    """Create a graph database schema.

    :param module_import:
    :param models_iterable:
    :param output_file:
    :param remove_schema_maker:
    :param schema_vertex_identifier:
    :return:
    """
    iterable = get_iterable_from_module(module_import, models_iterable)
    # TODO: edge cardinality
    # TODO: edge label multiplicity
    # TODO: remove_schema_maker
    # TODO: schema_vertex_identifier

    edge_labels = {}
    vertex_labels = {}
    properties = {}
    for model_class in iterable:
        if issubclass(model_class, Vertex):
            existing_vertex_label = vertex_labels.get(model_class.__label__)
            if existing_vertex_label:
                raise MultipleLabelsError(f"Vertex label {model_class.__label__!r} found multiple times - "
                                          f"in class {model_class!r} and {existing_vertex_label!r}")
            vertex_labels[model_class.__label__] = model_class
        elif issubclass(model_class, Edge):
            existing_edge_label = edge_labels.get(model_class.__label__)
            if existing_edge_label:
                raise MultipleLabelsError(f"Edge label {model_class.__label__!r} found multiple times - "
                                          f"in class {model_class!r} and {existing_vertex_label!r}")
            edge_labels[model_class.__label__] = model_class
        else:
            raise InvalidElementError(f"Element {model_class.__name__} from {module_import} present in "
                                      f"iterable {models_iterable} is not of type "
                                      f"goblin.element.Edge nor goblin.element.Vertex")

        for property_name, property_instance in model_class.__properties__.items():
            if not isinstance(property_instance, (Property, VertexProperty)):
                _LOGGER.warning(f"Skipping property {property_name!r}, not of type Property nor VertexProperty")
                continue

            if isinstance(property_instance, Property) and issubclass(model_class, Vertex):
                raise WrongPropertyType(f"Property {property_name!r} in {model_class} is of "
                                        f"type {type(property_instance)}, but should be of type VertexProperty.")
            elif isinstance(property_instance, VertexProperty) and issubclass(model_class, Edge):
                raise WrongPropertyType(f"Property {property_name!r} in {model_class} is of "
                                        f"type {type(property_instance)}, but should be of type Property.")

            db_name = property_instance.getdb_name() or property_name
            properties[db_name] = properties.get(db_name, []) + [property_instance]

    with open(output_file, 'w') as output:
        output.write("mgmt = graph.openManagement()\n\n")

        for vertex_label in vertex_labels.keys():
            output.write(f"if (mgmt.getVertexLabel('{vertex_label}') == null)\n"
                         f"  mgmt.makeVertexLabel('{vertex_label}').make()\n")

        output.write('\n')

        for edge_label in edge_labels.keys():
            output.write(f"if (mgmt.getEdgeLabel('{edge_label}') == null)\n"
                         f"  mgmt.makeEdgeLabel('{edge_label}').make()\n")

        output.write('\n')

        for property_db_name, property_instances in properties.items():
            property_type = _get_property_type(property_instances[0])
            property_cardinality = None
            if isinstance(property_instances[0], VertexProperty):
                property_cardinality = _get_property_cardinality(property_instances[0])

            for property_instance in property_instances[1:]:
                next_property_type = _get_property_type(property_instance)
                if next_property_type != property_type:
                    raise ValueError("Property type does not match for classes ... and class")

                if isinstance(property_instance, VertexProperty):
                    next_property_cardinality = _get_property_cardinality(property_instance)
                    property_cardinality = property_cardinality or next_property_cardinality
                    if next_property_cardinality != property_cardinality:
                        raise ValueError

            output.write(f"if (mgmt.getPropertyKey('{property_db_name}') == null)\n"
                         f"  mgmt.makePropertyKey('{property_db_name}').dataType({property_type})")
            if property_cardinality:
                output.write(f".cardinality({property_cardinality})")
            output.write(f".make()\n\n")

        output.write(f"if (mgmt.getPropertyKey('__label__') == null)\n"
                     f"  mgmt.makePropertyKey('__label__').dataType({property_type})"
                     f".cardinality(Cardinality.SINGLE).make()\n\n")

        output.write(f"if (mgmt.getPropertyKey('__type__') == null)\n"
                     f"  mgmt.makePropertyKey('__type__').dataType({property_type})"
                     f".cardinality(Cardinality.SINGLE).make()\n\n")

        output.write("\nmgmt.commit()\n")
