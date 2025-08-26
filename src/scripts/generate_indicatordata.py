import json
import pandas as pd
from json2html import *

data_path = "data/indicators.json"
outfile_path = "docs/indicatordata.md"
outfile_path_short = "docs/indicatordata"

json_file = open(data_path)
json_data = json.load(json_file)
json_file.close

df = pd.read_json(data_path)

for i in range(len(json_data)):
    record = json_data[i]   
    html_record = json2html.convert(json=record)
    with open(outfile_path_short + str(i) + ".md", "w") as md_record:
         md_record.write(html_record)

tab_data = df[["name", "key_area", "thematic_area", "domain"]]

tab_data.loc[:, "name"] = '<a href="#" onClick="MyWindow=window.open(\'../indicatordata' + tab_data.index.astype(str) + '/\',\'' + tab_data["name"] + '\',\'width=1500,height=1500\'); return false;">' + tab_data["name"] + '</a><br>'

with open(outfile_path, "a") as md:
    tab_data.to_markdown(buf = md, index = False, tablefmt = "github")
