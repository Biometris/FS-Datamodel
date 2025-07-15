# Auto generated from food_system_indicators.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-04-21T17:03:00
# Schema: food-system-indicators
#
# id: https://w3id.org/linkml/examples/fsi
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Double, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
IAO = CurieNamespace('IAO', 'http://purl.obolibrary.org/obo/IAO_')
UO = CurieNamespace('UO', 'http://example.org/UNKNOWN/UO/')
DCT = CurieNamespace('dct', 'http://purl.org/dc/terms/')
FSI = CurieNamespace('fsi', 'https://w3id.org/linkml/examples/fsi')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OBO = CurieNamespace('obo', 'http://purl.obolibrary.org/obo/')
QUDT = CurieNamespace('qudt', 'http://qudt.org/schema/qudt/')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = FSI


# Types
class IriType(Uriorcurie):
    """ An IRI """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "iri type"
    type_model_uri = FSI.IriType


class LabelType(String):
    """ A string that provides a human-readable name for an entity """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "label type"
    type_model_uri = FSI.LabelType


class NarrativeText(String):
    """ A string that provides a human-readable description of something """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "narrative text"
    type_model_uri = FSI.NarrativeText


class Unit(String):
    type_class_uri = UO["0000000"]
    type_class_curie = "UO:0000000"
    type_name = "unit"
    type_model_uri = FSI.Unit


# Class references
class EntityId(extended_str):
    pass


class NamedThingId(EntityId):
    pass


class IndicatorId(NamedThingId):
    pass


class QuantityValueId(NamedThingId):
    pass


@dataclass(repr=False)
class Entity(YAMLRoot):
    """
    Root class for all things and informational relationships, real or imagined.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FSI["Entity"]
    class_class_curie: ClassVar[str] = "fsi:Entity"
    class_name: ClassVar[str] = "entity"
    class_model_uri: ClassVar[URIRef] = FSI.Entity

    id: Union[str, EntityId] = None
    iri: Optional[Union[str, IriType]] = None
    name: Optional[Union[str, LabelType]] = None
    description: Optional[Union[str, NarrativeText]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EntityId):
            self.id = EntityId(self.id)

        if self.iri is not None and not isinstance(self.iri, IriType):
            self.iri = IriType(self.iri)

        if self.name is not None and not isinstance(self.name, LabelType):
            self.name = LabelType(self.name)

        if self.description is not None and not isinstance(self.description, NarrativeText):
            self.description = NarrativeText(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class NamedThing(Entity):
    """
    A databased entity or concept/class.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FSI["NamedThing"]
    class_class_curie: ClassVar[str] = "fsi:NamedThing"
    class_name: ClassVar[str] = "named thing"
    class_model_uri: ClassVar[URIRef] = FSI.NamedThing

    id: Union[str, NamedThingId] = None
    category: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        if not isinstance(self.category, str):
            self.category = str(self.category)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Indicator(NamedThing):
    """
    Food system indicator.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FSI["Indicator"]
    class_class_curie: ClassVar[str] = "fsi:Indicator"
    class_name: ClassVar[str] = "indicator"
    class_model_uri: ClassVar[URIRef] = FSI.Indicator

    id: Union[str, IndicatorId] = None
    category: str = None
    name: str = None
    description: str = None
    spatial_scope: Union[str, "SpatialScopeTypes"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IndicatorId):
            self.id = IndicatorId(self.id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, str):
            self.description = str(self.description)

        if self._is_empty(self.spatial_scope):
            self.MissingRequiredField("spatial_scope")
        if not isinstance(self.spatial_scope, SpatialScopeTypes):
            self.spatial_scope = SpatialScopeTypes(self.spatial_scope)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class QuantityValue(NamedThing):
    """
    A value of an attribute that is quantitative and measurable, expressed as a combination of a unit and a numeric
    value
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FSI["QuantityValue"]
    class_class_curie: ClassVar[str] = "fsi:QuantityValue"
    class_name: ClassVar[str] = "quantity value"
    class_model_uri: ClassVar[URIRef] = FSI.QuantityValue

    id: Union[str, QuantityValueId] = None
    category: str = None
    has_unit: Optional[Union[str, Unit]] = None
    has_numeric_value: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, QuantityValueId):
            self.id = QuantityValueId(self.id)

        if self.has_unit is not None and not isinstance(self.has_unit, Unit):
            self.has_unit = Unit(self.has_unit)

        if self.has_numeric_value is not None and not isinstance(self.has_numeric_value, float):
            self.has_numeric_value = float(self.has_numeric_value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Datapoint(QuantityValue):
    """
    Food system indicator datapoint.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FSI["Datapoint"]
    class_class_curie: ClassVar[str] = "fsi:Datapoint"
    class_name: ClassVar[str] = "datapoint"
    class_model_uri: ClassVar[URIRef] = FSI.Datapoint

    category: str = None
    id: Optional[str] = None
    datapoint_of: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.datapoint_of is not None and not isinstance(self.datapoint_of, str):
            self.datapoint_of = str(self.datapoint_of)

        super().__post_init__(**kwargs)


# Enumerations
class SpatialScopeTypes(EnumDefinitionImpl):

    Eu = PermissibleValue(
        text="Eu",
        description="EU wide")
    EuMemberStates = PermissibleValue(
        text="EuMemberStates",
        description="...")
    Regional = PermissibleValue(
        text="Regional",
        description="...")
    Local = PermissibleValue(
        text="Local",
        description="...")

    _defn = EnumDefinition(
        name="SpatialScopeTypes",
    )

# Slots
class slots:
    pass

slots.node_property = Slot(uri=FSI.node_property, name="node property", curie=FSI.curie('node_property'),
                   model_uri=FSI.node_property, domain=NamedThing, range=Optional[str])

slots.description = Slot(uri=DCT.description, name="description", curie=DCT.curie('description'),
                   model_uri=FSI.description, domain=None, range=Optional[Union[str, NarrativeText]])

slots.has_numeric_value = Slot(uri=FSI.has_numeric_value, name="has numeric value", curie=FSI.curie('has_numeric_value'),
                   model_uri=FSI.has_numeric_value, domain=QuantityValue, range=Optional[float])

slots.has_unit = Slot(uri=FSI.has_unit, name="has unit", curie=FSI.curie('has_unit'),
                   model_uri=FSI.has_unit, domain=QuantityValue, range=Optional[Union[str, Unit]])

slots.id = Slot(uri=FSI.id, name="id", curie=FSI.curie('id'),
                   model_uri=FSI.id, domain=Entity, range=Union[str, EntityId])

slots.iri = Slot(uri=FSI.iri, name="iri", curie=FSI.curie('iri'),
                   model_uri=FSI.iri, domain=None, range=Optional[Union[str, IriType]])

slots.datapoint_of = Slot(uri=FSI.datapoint_of, name="datapoint of", curie=FSI.curie('datapoint_of'),
                   model_uri=FSI.datapoint_of, domain=NamedThing, range=Union[str, IndicatorId])

slots.name = Slot(uri=RDFS.label, name="name", curie=RDFS.curie('label'),
                   model_uri=FSI.name, domain=Entity, range=Optional[Union[str, LabelType]])

slots.synonym = Slot(uri=FSI.synonym, name="synonym", curie=FSI.curie('synonym'),
                   model_uri=FSI.synonym, domain=NamedThing, range=Optional[Union[Union[str, LabelType], List[Union[str, LabelType]]]])

slots.indicator__id = Slot(uri=SCHEMA.id, name="indicator__id", curie=SCHEMA.curie('id'),
                   model_uri=FSI.indicator__id, domain=None, range=URIRef)

slots.indicator__name = Slot(uri=SCHEMA.name, name="indicator__name", curie=SCHEMA.curie('name'),
                   model_uri=FSI.indicator__name, domain=None, range=str)

slots.indicator__description = Slot(uri=SCHEMA.description, name="indicator__description", curie=SCHEMA.curie('description'),
                   model_uri=FSI.indicator__description, domain=None, range=str)

slots.indicator__spatial_scope = Slot(uri=FSI.spatial_scope, name="indicator__spatial_scope", curie=FSI.curie('spatial_scope'),
                   model_uri=FSI.indicator__spatial_scope, domain=None, range=Union[str, "SpatialScopeTypes"])

slots.datapoint__id = Slot(uri=FSI.id, name="datapoint__id", curie=FSI.curie('id'),
                   model_uri=FSI.datapoint__id, domain=None, range=Optional[str])

slots.datapoint__datapoint_of = Slot(uri=FSI.datapoint_of, name="datapoint__datapoint_of", curie=FSI.curie('datapoint_of'),
                   model_uri=FSI.datapoint__datapoint_of, domain=None, range=Optional[str])

slots.category = Slot(uri=FSI.category, name="category", curie=FSI.curie('category'),
                   model_uri=FSI.category, domain=None, range=str)

slots.named_thing_category = Slot(uri=FSI.category, name="named thing_category", curie=FSI.curie('category'),
                   model_uri=FSI.named_thing_category, domain=NamedThing, range=str)