-- # Class: "indicator" Description: "Food system indicator."
--     * Slot: id Description: unique identifier of the indicator
--     * Slot: name Description: denomination of the indicator
--     * Slot: description Description: concise text that provides the meaning of the identifier
--     * Slot: spatial_scope Description: reference to the spatial unit that the indicator describes
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
-- # Class: "datapoint" Description: "Food system indicator datapoint."
--     * Slot: uid Description: 
--     * Slot: id Description: 
--     * Slot: datapoint_of Description: 
--     * Slot: has_unit Description: connects a quantity value to a unit
--     * Slot: has_numeric_value Description: connects a quantity value to a number
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: A human-readable name for an attribute or entity.
--     * Slot: description Description: A human-readable description of an entity.
-- # Class: "quantity value" Description: "A value of an attribute that is quantitative and measurable, expressed as a combination of a unit and a numeric value"
--     * Slot: has_unit Description: connects a quantity value to a unit
--     * Slot: has_numeric_value Description: connects a quantity value to a number
--     * Slot: id Description: A unique identifier for an entity.
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: A human-readable name for an attribute or entity.
--     * Slot: description Description: A human-readable description of an entity.
-- # Class: "entity" Description: "Root class for all things and informational relationships, real or imagined."
--     * Slot: id Description: A unique identifier for an entity.
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: A human-readable name for an attribute or entity.
--     * Slot: description Description: A human-readable description of an entity.
-- # Class: "named thing" Description: "A databased entity or concept/class."
--     * Slot: id Description: A unique identifier for an entity.
--     * Slot: iri Description: An IRI for an entity. This is determined by the id using expansion rules.
--     * Slot: name Description: A human-readable name for an attribute or entity.
--     * Slot: description Description: A human-readable description of an entity.

CREATE TABLE indicator (
	id TEXT NOT NULL, 
	name TEXT NOT NULL, 
	description TEXT NOT NULL, 
	spatial_scope VARCHAR(14) NOT NULL, 
	iri TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE datapoint (
	uid INTEGER NOT NULL, 
	id TEXT, 
	datapoint_of TEXT, 
	has_unit TEXT, 
	has_numeric_value FLOAT, 
	iri TEXT, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (uid)
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