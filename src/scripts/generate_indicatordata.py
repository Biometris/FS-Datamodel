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

    indicator_name = df["name"].iloc[i]
         
    with open(outfile_path, "a") as md:
        md.write('<a href="#" onClick="MyWindow=window.open(\'../indicatordata' + str(i) + '/\',\'' + indicator_name + 
                 '\',\'width=1100,height=1500\'); return false;">' + indicator_name + '</a><br>') 



