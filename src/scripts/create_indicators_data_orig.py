import sys
from dataclasses import dataclass
from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader
import yaml

from linkml_runtime.utils.yamlutils import as_dict
sys.path.append("./")
import project.food_system_indicators as fsi

data_path = "data/indicators.yaml"

@dataclass
class Entity:
    id: str
    name: str
    key_area: str
    thematic_area: str

def get_thematic_area(key_area, thematic_area_id):
    match key_area.code:
        case fsi.SustainabilityDimension.Environmental:
            return fsi.EnvironmentalThematicArea(thematic_area_id)
        case fsi.SustainabilityDimension.Economic:
            return fsi.EconomicThematicArea(thematic_area_id)
        case fsi.SustainabilityDimension.Social:
            return fsi.SocialThematicArea(thematic_area_id)
        case fsi.SustainabilityDimension.Horizontal:
            return fsi.HorizontalThematicArea(thematic_area_id)
        case _:
            return None

def read_indicator_data(path):
    # Load data as a list of dicts
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Convert each dict into an indicator
    indicators = [fsi.Indicator(**as_dict(d)) for d in data]
    return indicators

def create_indicator_records(indicators):
    # Create table records
    entities = []
    for indicator in indicators:
        thematic_area = get_thematic_area(
            indicator.key_area,
            indicator.thematic_area
        )
        entities.append(
            Entity(
                indicator.id,
                indicator["name"],
                str(indicator.key_area._code.description),
                str(thematic_area._code.description)
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

indicators = read_indicator_data(data_path)
records = create_indicator_records(indicators)
create_indicator_hiearchy_json(records)
create_indicators_data_table(records)
