# Convert the indicator data provided in yaml format to data in json format.
# The json format is required for easy conversion to html/docs.

import yaml
import json

data_path_in = "data/indicators.yaml"
data_path_out = "data/indicators.json"

with open(data_path_in, 'r') as yaml_in, open(data_path_out, "w") as json_out:
    yaml_object = yaml.safe_load(yaml_in) 
    json.dump(yaml_object, json_out, indent = "\t")