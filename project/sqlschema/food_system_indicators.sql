-- # Abstract Class: "entity" Description: "Root class for all things and informational relationships, real or imagined."
--     * Slot: id Description: A unique identifier for an entity.
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: A human-readable name for an attribute or entity.
--     * Slot: description Description: A human-readable description of an entity.
-- # Class: "named thing" Description: "A databased entity or concept/class."
--     * Slot: id Description: A unique identifier for an entity.
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: A human-readable name for an attribute or entity.
--     * Slot: description Description: A human-readable description of an entity.
-- # Class: "indicator" Description: "Food system indicator."
--     * Slot: spatial_scope Description: Reference to the spatial unit that the indicator describes
--     * Slot: id Description: unique identifier of the indicator
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: denomination of the indicator
--     * Slot: description Description: concise text that provides the meaning of the identifier
-- # Class: "indicator datapoint" Description: "Food system indicator datapoint."
--     * Slot: measurement_of Description: Indicator
--     * Slot: has_unit Description: connects a quantity value to a unit
--     * Slot: has_numeric_value Description: connects a quantity value to a number
--     * Slot: id Description: unique identifier of the datapoint
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: A human-readable name for an attribute or entity.
--     * Slot: description Description: A human-readable description of an entity.
--     * Slot: indicator datapoint collection_id Description: Autocreated FK slot
-- # Class: "indicator datapoint collection" Description: "Collection of food system indicator datapoints."
--     * Slot: id Description: 
-- # Class: "quantity value" Description: "A value of an attribute that is quantitative and measurable, expressed as a combination of a unit and a numeric value"
--     * Slot: has_unit Description: connects a quantity value to a unit
--     * Slot: has_numeric_value Description: connects a quantity value to a number
--     * Slot: id Description: A unique identifier for an entity.
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: A human-readable name for an attribute or entity.
--     * Slot: description Description: A human-readable description of an entity.

CREATE TABLE entity (
	id TEXT NOT NULL, 
	iri TEXT, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "named thing" (
	id TEXT NOT NULL, 
	iri TEXT, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE indicator (
	spatial_scope VARCHAR(14) NOT NULL, 
	id TEXT NOT NULL, 
	iri TEXT, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "indicator datapoint collection" (
	id INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE "quantity value" (
	has_unit TEXT, 
	has_numeric_value FLOAT, 
	id TEXT NOT NULL, 
	iri TEXT, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "indicator datapoint" (
	measurement_of TEXT NOT NULL, 
	has_unit TEXT, 
	has_numeric_value FLOAT, 
	id TEXT NOT NULL, 
	iri TEXT, 
	name TEXT, 
	description TEXT, 
	"indicator datapoint collection_id" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(measurement_of) REFERENCES indicator (id), 
	FOREIGN KEY("indicator datapoint collection_id") REFERENCES "indicator datapoint collection" (id)
);