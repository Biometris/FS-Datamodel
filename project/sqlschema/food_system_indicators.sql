-- # Abstract Class: "Entity" Description: "Root class for all things and informational relationships, real or imagined."
--     * Slot: id Description: A unique identifier for an entity.
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: A human-readable name for an attribute or entity.
--     * Slot: description Description: A human-readable description of an entity.
-- # Class: "ThematicArea" Description: "a thematic area"
--     * Slot: id Description: 
-- # Class: "Indicator" Description: "Food system indicator."
--     * Slot: spatial_scope Description: Reference to the spatial unit that the indicator describes
--     * Slot: key_area Description: Reference to the thematic area that the indicator belongs to
--     * Slot: id Description: unique identifier of the indicator
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: denomination of the indicator
--     * Slot: description Description: concise text that provides the meaning of the identifier
--     * Slot: thematic_area_id Description: the thematic area the indicator belongs to
-- # Class: "IndicatorDatapoint" Description: "Food system indicator datapoint."
--     * Slot: measurement_of Description: Indicator
--     * Slot: has_unit Description: connects a quantity value to a unit
--     * Slot: has_numeric_value Description: connects a quantity value to a number
--     * Slot: id Description: unique identifier of the datapoint
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: A human-readable name for an attribute or entity.
--     * Slot: description Description: A human-readable description of an entity.
--     * Slot: IndicatorDatapointCollection_id Description: Autocreated FK slot
-- # Class: "IndicatorDatapointCollection" Description: "Collection of food system indicator datapoints."
--     * Slot: id Description: 
-- # Class: "QuantityValue" Description: "A value of an attribute that is quantitative and measurable, expressed as a combination of a unit and a numeric value"
--     * Slot: has_unit Description: connects a quantity value to a unit
--     * Slot: has_numeric_value Description: connects a quantity value to a number
--     * Slot: id Description: A unique identifier for an entity.
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: A human-readable name for an attribute or entity.
--     * Slot: description Description: A human-readable description of an entity.

CREATE TABLE "Entity" (
	id TEXT NOT NULL, 
	iri TEXT, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "ThematicArea" (
	id INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE "IndicatorDatapointCollection" (
	id INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE "QuantityValue" (
	has_unit TEXT, 
	has_numeric_value FLOAT, 
	id TEXT NOT NULL, 
	iri TEXT, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "Indicator" (
	spatial_scope VARCHAR(14) NOT NULL, 
	key_area VARCHAR(13) NOT NULL, 
	id TEXT NOT NULL, 
	iri TEXT, 
	name TEXT, 
	description TEXT, 
	thematic_area_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(thematic_area_id) REFERENCES "ThematicArea" (id)
);
CREATE TABLE "IndicatorDatapoint" (
	measurement_of TEXT NOT NULL, 
	has_unit TEXT, 
	has_numeric_value FLOAT, 
	id TEXT NOT NULL, 
	iri TEXT, 
	name TEXT, 
	description TEXT, 
	"IndicatorDatapointCollection_id" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(measurement_of) REFERENCES "Indicator" (id), 
	FOREIGN KEY("IndicatorDatapointCollection_id") REFERENCES "IndicatorDatapointCollection" (id)
);