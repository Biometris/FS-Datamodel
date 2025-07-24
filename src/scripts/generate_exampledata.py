import pandas as pd

data_path = "data/indicators.csv"
outfile_path = "docs/exampledata.md"

df = pd.read_csv(data_path)
df = df[["name", "description", "key_area" , "thematic_area"]]
df.rename(columns = {"key_area": "key area", "thematic_area": "thematic area"}, inplace = True)

with open(outfile_path, "w") as md:
    df.to_markdown(buf = md, index = False, tablefmt = "github")