import json
import pandas as pd
import itables
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

tab_data = df
tab_data.loc[:, "name"] = '<a href="#" onClick="MyWindow=window.open(\'../indicatordata' + tab_data.index.astype(str) + '/\',\'' + tab_data["name"] + '\',\'width=1500,height=1500\'); return false;">' + tab_data["name"] + '</a><br>'

vis_cols = ["name", "key_area", "thematic_area", "domain"]
vis_cols_ind = tab_data.columns.get_indexer(vis_cols).tolist()

tab_html = itables.to_html_datatable(tab_data,
                                     allow_html=True,
                                     search={"regex": True, "caseInsensitive": True},
                                     buttons=["pageLength", "colvis", "csvHtml5", "excelHtml5"],
                                     lengthMenu=[2, 5, 10, 20, 50],
                                     pageLength=10,
                                     layout={"top1": "searchBuilder"},
                                     columnDefs=[{"targets": vis_cols_ind, "visible": True},
                                                 {"targets": "_all", "visible": False }]
                                    )
with open(outfile_path, "a") as md:
     md.write("The table below gives an overview of all the indicators." + "<br><br>" + 
              "Search through them by using the search box, for searching across all columns." +
              "Alternatively, construct a more complex search query by adding conditions on separate columns in the custom search builder." + "<br><br>" +
              "Use the column visibility dropdown menu to show additional columns." + "<br><br>" +
              "Use the csv and excel buttons for exporting the (filtered) indicators to a .csv or .excel file respectively." +
              "When exporting data all columns will be included in the export, even those that are not visible." + "<br><br>" +
              "Click on the name of an indicator to open a popup with all information available for the that indicator.")
     md.write(tab_html)