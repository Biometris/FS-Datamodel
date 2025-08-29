import sys
import json
import yaml
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass
from typing import List

from linkml_runtime.utils.yamlutils import as_dict
sys.path.append("./")
import project.food_system_indicators as fsi

data_path = "data/indicators.yaml"
outfile_path = "docs/indicators_table.md"

@dataclass
class Entity:
    id: str
    name: str
    SustainabilityDimension: fsi.SustainabilityDimension

# Load data as a list of dicts
with open(data_path) as f:
    data = yaml.safe_load(f)

# Convert each dict into an indicator
indicators = [fsi.Indicator(**as_dict(d)) for d in data]

# Create table records
entities = []
for indicator in indicators:
    for ds in indicator.data_source:
        entities.append(
            Entity(
                indicator.id,
                indicator.name,
                indicator.key_area
            ))

# point to templates folder
env = Environment(loader=FileSystemLoader("./src/scripts/templates"))
template = env.get_template("indicators-table.md.j2")

# Render
markdown_output = template.render(entities=entities)

# Save to file
with open(outfile_path, "w") as f:
    f.write(markdown_output)
