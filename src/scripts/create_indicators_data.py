from dataclasses import dataclass
from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader
from linkml_store.api.client import Client
from linkml_runtime import SchemaView
from linkml_store.utils.format_utils import load_objects

schema_path = "src/schema/food_system_indicators.yaml"

indicator_data_path = "data/indicators.yaml"
database_data_path = "data/databases.yaml"

## Setup database
client = Client()
db = client.attach_database("duckdb", alias="fsidb")
sv = SchemaView(schema_path)
db.set_schema_view(sv)

## Add data to database.
database_collection = db.create_collection("Database", "Databases")
database_obs = load_objects(database_data_path)
database_collection.insert(database_obs)

for r in database_collection.iter_validate_collection():
   print(r.message)

indicator_collection = db.create_collection("Indicator", "Indicators")
indicator_obs = load_objects(indicator_data_path)
indicator_collection.insert(indicator_obs)

for r in indicator_collection.iter_validate_collection():
   print(r.message)   

results = list(db.iter_validate_database(ensure_referential_integrity=True))
for result in results:
    print(result)

@dataclass
class Entity:
    id: str
    name: str
    key_area: str
    thematic_area: str

def create_indicator_records(indicator_collection):

    thematic_areas = db.schema_view.get_element("thematic_area").__getattribute__("any_of")
    all_thematic_areas = {}
    for thematic_area in thematic_areas:
        range = getattr(thematic_area, "range")
        permissible_range = db.schema_view.get_enum(range).permissible_values
        all_thematic_areas.update(permissible_range)

    all_key_areas = db.schema_view.get_enum("SustainabilityDimension").permissible_values

    # Create table records
    entities = []
    for indicator in indicator_collection.rows_iter():
        thematic_area = all_thematic_areas[indicator.get("thematic_area")]
        key_area = all_key_areas[indicator.get("key_area")]
        entities.append(
            Entity(
                indicator.get("id"),
                indicator.get("name"),
                getattr(key_area, "description"),
                getattr(thematic_area, "description")
            ))
    return entities

def create_indicator_hiearchy_json(entities):
    # Output file
    outfile_path = "docs/data/indicators_chart_data.json"

    # Build hierarchy
    hierarchy = {}
    for e in entities:
        if e.key_area not in hierarchy:
            hierarchy[e.key_area] = {}
        if e.thematic_area not in hierarchy[e.key_area]:
            hierarchy[e.key_area][e.thematic_area] = []
        hierarchy[e.key_area][e.thematic_area].append(e)

    # Convert hierarchy
    sunburst_data = []
    for key_area, thematic_groups in hierarchy.items():
        key_area_node = {"name": key_area, "children": []}
        for thematic_area_id, ents in thematic_groups.items():
            thematic_node = {
                "name": thematic_area_id,
                "children": [{"name": ent.name, "value": 1} for ent in ents]
            }
            key_area_node["children"].append(thematic_node)
        sunburst_data.append(key_area_node)

    # Save JSON for reuse
    Path(outfile_path).write_text(json.dumps(sunburst_data, indent=2))

def create_indicators_data_table(entities):
    # Out file
    output_file = "docs/indicators_table.md"

    # Point to templates folder
    env = Environment(loader=FileSystemLoader("./src/docs/templates"))
    template = env.get_template("indicators_table.md.j2")

    # Render
    markdown_output = template.render(entities=entities)

    # Save to file
    with open(output_file, "w") as f:
        f.write(markdown_output)

def create_databases_data_table(database_collection):
    # Out file
    output_file = "docs/databases_table.md"

    # Point to templates folder
    env = Environment(loader=FileSystemLoader("./src/docs/templates"))
    template = env.get_template("databases_table.md.j2")

    # Render
    markdown_output = template.render(collection=database_collection)

    # Save to file
    with open(output_file, "w") as f:
        f.write(markdown_output)


records = create_indicator_records(indicator_collection)
create_indicator_hiearchy_json(records)
create_indicators_data_table(records)

create_databases_data_table(database_collection)