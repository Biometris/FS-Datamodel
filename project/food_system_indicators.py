# Auto generated from food_system_indicators.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-07-25T16:30:37
# Schema: food_system_indicators
#
# id: https://w3id.org/linkml/examples/fsi
# description: Model for the indicators on the sustainability performance of food Systems within Europe.
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

# Namespaces
IAO = CurieNamespace('IAO', 'http://purl.obolibrary.org/obo/IAO_')
UO = CurieNamespace('UO', 'http://purl.obolibrary.org/obo/UO_')
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
    type_name = "iri_type"
    type_model_uri = FSI.IriType


class LabelType(String):
    """ A string that provides a human-readable name for an entity """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "label_type"
    type_model_uri = FSI.LabelType


class NarrativeText(String):
    """ A string that provides a human-readable description of something """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "narrative_text"
    type_model_uri = FSI.NarrativeText


class Unit(String):
    type_class_uri = UO["0000000"]
    type_class_curie = "UO:0000000"
    type_name = "unit"
    type_model_uri = FSI.Unit


# Class references
class EntityId(extended_str):
    pass


class IndicatorId(EntityId):
    pass


class QuantityValueId(EntityId):
    pass


class IndicatorDatapointId(QuantityValueId):
    pass


@dataclass(repr=False)
class Entity(YAMLRoot):
    """
    Root class for all things and informational relationships, real or imagined.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FSI["Entity"]
    class_class_curie: ClassVar[str] = "fsi:Entity"
    class_name: ClassVar[str] = "Entity"
    class_model_uri: ClassVar[URIRef] = FSI.Entity

    id: Union[str, EntityId] = None
    iri: Optional[Union[str, IriType]] = None
    name: Optional[Union[str, LabelType]] = None
    description: Optional[Union[str, NarrativeText]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
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


ThematicArea = Any

@dataclass(repr=False)
class Indicator(Entity):
    """
    Food system indicator.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FSI["Indicator"]
    class_class_curie: ClassVar[str] = "fsi:Indicator"
    class_name: ClassVar[str] = "Indicator"
    class_model_uri: ClassVar[URIRef] = FSI.Indicator

    id: Union[str, IndicatorId] = None
    spatial_scope: Union[str, "SpatialScopeType"] = None
    key_area: Union[str, "SustainabilityDimension"] = None
    thematic_area: Union[dict, ThematicArea] = None
    name: Optional[Union[str, LabelType]] = None
    description: Optional[Union[str, NarrativeText]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IndicatorId):
            self.id = IndicatorId(self.id)

        if self._is_empty(self.spatial_scope):
            self.MissingRequiredField("spatial_scope")
        if not isinstance(self.spatial_scope, SpatialScopeType):
            self.spatial_scope = SpatialScopeType(self.spatial_scope)

        if self._is_empty(self.key_area):
            self.MissingRequiredField("key_area")
        if not isinstance(self.key_area, SustainabilityDimension):
            self.key_area = SustainabilityDimension(self.key_area)

        if self.name is not None and not isinstance(self.name, LabelType):
            self.name = LabelType(self.name)

        if self.description is not None and not isinstance(self.description, NarrativeText):
            self.description = NarrativeText(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class IndicatorDatapointCollection(YAMLRoot):
    """
    Collection of food system indicator datapoints.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FSI["IndicatorDatapointCollection"]
    class_class_curie: ClassVar[str] = "fsi:IndicatorDatapointCollection"
    class_name: ClassVar[str] = "IndicatorDatapointCollection"
    class_model_uri: ClassVar[URIRef] = FSI.IndicatorDatapointCollection

    indicator_datapoints: Optional[Union[dict[Union[str, IndicatorDatapointId], Union[dict, "IndicatorDatapoint"]], list[Union[dict, "IndicatorDatapoint"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="indicator_datapoints", slot_type=IndicatorDatapoint, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class QuantityValue(Entity):
    """
    A value of an attribute that is quantitative and measurable, expressed as a combination of a unit and a numeric
    value
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FSI["QuantityValue"]
    class_class_curie: ClassVar[str] = "fsi:QuantityValue"
    class_name: ClassVar[str] = "QuantityValue"
    class_model_uri: ClassVar[URIRef] = FSI.QuantityValue

    id: Union[str, QuantityValueId] = None
    has_unit: Optional[Union[str, Unit]] = None
    has_numeric_value: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
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
class IndicatorDatapoint(QuantityValue):
    """
    Food system indicator datapoint.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FSI["IndicatorDatapoint"]
    class_class_curie: ClassVar[str] = "fsi:IndicatorDatapoint"
    class_name: ClassVar[str] = "IndicatorDatapoint"
    class_model_uri: ClassVar[URIRef] = FSI.IndicatorDatapoint

    id: Union[str, IndicatorDatapointId] = None
    measurement_of: Union[str, IndicatorId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IndicatorDatapointId):
            self.id = IndicatorDatapointId(self.id)

        if self._is_empty(self.measurement_of):
            self.MissingRequiredField("measurement_of")
        if not isinstance(self.measurement_of, IndicatorId):
            self.measurement_of = IndicatorId(self.measurement_of)

        super().__post_init__(**kwargs)


# Enumerations
class SustainabilityDimension(EnumDefinitionImpl):
    """
    Main sustainability dimension.
    """
    Environmental = PermissibleValue(
        text="Environmental",
        description="environmental")
    Economic = PermissibleValue(
        text="Economic",
        description="economic")
    Social = PermissibleValue(
        text="Social",
        description="social")
    Horizontal = PermissibleValue(
        text="Horizontal",
        description="horizontal thematic areas")

    _defn = EnumDefinition(
        name="SustainabilityDimension",
        description="Main sustainability dimension.",
    )

class EnvironmentalThematicArea(EnumDefinitionImpl):
    """
    Enviromental sustainability dimension.
    """
    ClimateChange = PermissibleValue(
        text="ClimateChange",
        description="climate change")
    PollutionAntimicrobials = PermissibleValue(
        text="PollutionAntimicrobials",
        description="pollution and antimicrobials")
    SustainableUseOfResources = PermissibleValue(
        text="SustainableUseOfResources",
        description="sustainable use of resources")
    Biodiversity = PermissibleValue(
        text="Biodiversity",
        description="biodiversity")
    CrossCuttingAreas = PermissibleValue(
        text="CrossCuttingAreas",
        description="cross-cutting areas")

    _defn = EnumDefinition(
        name="EnvironmentalThematicArea",
        description="Enviromental sustainability dimension.",
    )

class EconomicThematicArea(EnumDefinitionImpl):
    """
    Economic sustainability dimension.
    """
    FairEconomicViabilityInFoodValueChain = PermissibleValue(
        text="FairEconomicViabilityInFoodValueChain",
        description="fair economic viability in the food value chain")
    DevelopmentAndLogistics = PermissibleValue(
        text="DevelopmentAndLogistics",
        description="development and logistics")

    _defn = EnumDefinition(
        name="EconomicThematicArea",
        description="Economic sustainability dimension.",
    )

class SocialThematicArea(EnumDefinitionImpl):
    """
    Social sustainability dimension.
    """
    FairInclusiveAndEthicalFoodSystem = PermissibleValue(
        text="FairInclusiveAndEthicalFoodSystem",
        description="fair, inclusive and ethical food system")
    FoodEnvironment = PermissibleValue(
        text="FoodEnvironment",
        description="food environment")
    NutritionAndHealth = PermissibleValue(
        text="NutritionAndHealth",
        description="nutrition and health")

    _defn = EnumDefinition(
        name="SocialThematicArea",
        description="Social sustainability dimension.",
    )

class HorizontalThematicArea(EnumDefinitionImpl):
    """
    Horizontal sustainability dimension.
    """
    Governance = PermissibleValue(
        text="Governance",
        description="governance")
    Resilience = PermissibleValue(
        text="Resilience",
        description="resilience")

    _defn = EnumDefinition(
        name="HorizontalThematicArea",
        description="Horizontal sustainability dimension.",
    )

class SpatialScopeType(EnumDefinitionImpl):
    """
    The spatial scope for which the indicator is defined.
    """
    Eu = PermissibleValue(
        text="Eu",
        description="EU wide")
    EuMemberStates = PermissibleValue(
        text="EuMemberStates",
        description="EU member states")
    Regional = PermissibleValue(
        text="Regional",
        description="Regional")
    Local = PermissibleValue(
        text="Local",
        description="Local")

    _defn = EnumDefinition(
        name="SpatialScopeType",
        description="The spatial scope for which the indicator is defined.",
    )

# Slots
class slots:
    pass

slots.node_property = Slot(uri=FSI.node_property, name="node property", curie=FSI.curie('node_property'),
                   model_uri=FSI.node_property, domain=Entity, range=Optional[str])

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

slots.measurement_of = Slot(uri=FSI.measurement_of, name="measurement_of", curie=FSI.curie('measurement_of'),
                   model_uri=FSI.measurement_of, domain=Entity, range=Union[str, IndicatorId])

slots.name = Slot(uri=RDFS.label, name="name", curie=RDFS.curie('label'),
                   model_uri=FSI.name, domain=Entity, range=Optional[Union[str, LabelType]])

slots.spatial_scope = Slot(uri=FSI.spatial_scope, name="spatial_scope", curie=FSI.curie('spatial_scope'),
                   model_uri=FSI.spatial_scope, domain=None, range=Union[str, "SpatialScopeType"])

slots.key_area = Slot(uri=FSI.key_area, name="key_area", curie=FSI.curie('key_area'),
                   model_uri=FSI.key_area, domain=None, range=Union[str, "SustainabilityDimension"])

slots.thematic_area = Slot(uri=FSI.thematic_area, name="thematic_area", curie=FSI.curie('thematic_area'),
                   model_uri=FSI.thematic_area, domain=None, range=Union[dict, ThematicArea])

slots.indicatorDatapointCollection__indicator_datapoints = Slot(uri=FSI.indicator_datapoints, name="indicatorDatapointCollection__indicator_datapoints", curie=FSI.curie('indicator_datapoints'),
                   model_uri=FSI.indicatorDatapointCollection__indicator_datapoints, domain=None, range=Optional[Union[dict[Union[str, IndicatorDatapointId], Union[dict, IndicatorDatapoint]], list[Union[dict, IndicatorDatapoint]]]])

slots.Indicator_id = Slot(uri=FSI.id, name="Indicator_id", curie=FSI.curie('id'),
                   model_uri=FSI.Indicator_id, domain=Indicator, range=Union[str, IndicatorId])

slots.Indicator_name = Slot(uri=RDFS.label, name="Indicator_name", curie=RDFS.curie('label'),
                   model_uri=FSI.Indicator_name, domain=Indicator, range=Optional[Union[str, LabelType]])

slots.Indicator_description = Slot(uri=DCT.description, name="Indicator_description", curie=DCT.curie('description'),
                   model_uri=FSI.Indicator_description, domain=Indicator, range=Optional[Union[str, NarrativeText]])

slots.IndicatorDatapoint_id = Slot(uri=FSI.id, name="IndicatorDatapoint_id", curie=FSI.curie('id'),
                   model_uri=FSI.IndicatorDatapoint_id, domain=IndicatorDatapoint, range=Union[str, IndicatorDatapointId])