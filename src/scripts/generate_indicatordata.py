import json
from json2html import *

data_path = "data/indicators.json"
outfile_path = "docs/indicatordata.md"

json_file = open(data_path)
json_data = json.load(json_file)
json_file.close

html_content = json2html.convert(json=json_data)

with open(outfile_path, "w") as md:
    md.write(html_content)   
