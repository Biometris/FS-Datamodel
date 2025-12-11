import yaml
import pandas as pd
import re

input_files = {
    'economy': 'data/250821_dimension_economy.xlsx',
    'environment': 'data/250821_dimension_environment.xlsx',
    'health': 'data/250821_dimension_health.xlsx',
    'society': 'data/250821_dimension_society.xlsx',
}

fout_indicator_definitions = "data/indicators.yaml"
fout_indicator_category_definitions = "data/indicator_categories.yaml"
fout_databases = "data/databases.yaml"
fout_data_collection_details = "data/indicator_data_collection_details.yaml"

# Read all input files and combine their sheets into a single DataFrame
all_dfs = []
for dimension_key, fname in input_files.items():
    try:
        xlsx_content = pd.read_excel(fname, sheet_name=None, skiprows=2, true_values="x")
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {fname}")
    # Keep sheet name as 'category' and keep which input file/dimension it came from
    for sheet_name, df in xlsx_content.items():
        df = df.copy()
        df['category'] = sheet_name
        df['dimension'] = dimension_key
        all_dfs.append(df)

if not all_dfs:
    raise RuntimeError("No data frames were loaded from input files.")

# Combine all dataframes into one
xlsx_combined = pd.concat(all_dfs, ignore_index=True)
xlsx_combined = xlsx_combined[pd.notnull(xlsx_combined.get("Indicator"))]

# Remove spaces from all text fields
for column in xlsx_combined.columns:
    if xlsx_combined[column].dtype == "object":
        xlsx_combined[column] = xlsx_combined[column].map(lambda x : " ".join(x.split()) if isinstance(x, str) else x)

# Helper function to create identifiers
def to_identifier(xlsx_combined, column_name):
    result = xlsx_combined[column_name].str.title().replace("[^a-zA-Z0-9]", "", regex=True)
    result = result.str.slice(0, 50)
    return result

# Helper function to create identifiers
def escape(xlsx_combined, column_name):
    return xlsx_combined[column_name].str.replace("[“”]", "\"", regex=True)

# Helper function to create identifiers
def map_spatial_granularity(xlsx_combined):
    result = []
    for record in xlsx_combined["Data available on regional level?"]:
        items = ["Country"]
        if (record):
            items.append("NUTS1")
        result.append(items)
    return result

# Helper function to create identifiers
def map_sustainability_impact(xlsx_combined, column_name):
    # Map datapoints
    impact_mapping = {
        "-": "Negative",
        "+": "Positive"
    }
    result = []
    for record in xlsx_combined[column_name]:
        if isinstance(record, float):
            result.append("Undefined")
        else:
            record = re.sub("[^+-]", "", record)
            result.append(impact_mapping.get(record, "Undefined"))

    return result

# Map supply chain components
### TODO: This should ideally be correct in input. Check and throw error?
component_mapping = {
    "Connsumption": "Consumption",
    "RetailDistribution": "Retail"
}
supply_chain_components = []
for lst in xlsx_combined["Related stage of the food supply chain"].str.split("[;,]", regex=True):
    if isinstance(lst, float):
        supply_chain_components.append([])
    else:
        components = [(re.sub("[^a-zA-Z0-9]", "", str.title())) for str in lst]
        components = [component_mapping.get(component, component) for component in components]
        components = list(set(components)) if not isinstance(components[0], list) else components[0]
        supply_chain_components.append(components)

# Build the final indicator data structure
indicator_data = {
    "id": to_identifier(xlsx_combined, "Indicator"),
    "name": xlsx_combined["Indicator"],
    "description": escape(xlsx_combined, "Definition"),
    "definition": "",
    "measurement_unit": xlsx_combined["Unit"],
    "dimension": to_identifier(xlsx_combined, "dimension"),
    "has_category": to_identifier(xlsx_combined, "category"),
    "supply_chain_component": supply_chain_components,
    "sustainability_impact": map_sustainability_impact(xlsx_combined, "Impact on sustainability")
}

# Change data orientation
indicators = pd.DataFrame(indicator_data).to_dict(orient='records')

# Remove missing values.
indicators = [{i:j for i,j in indicator.items() if j == j} for indicator in indicators]

# Write to YAML
yaml_output = yaml.dump(indicators, sort_keys=False, indent=2, allow_unicode=True)
with open(fout_indicator_definitions, "w", encoding="utf-8") as f:
    f.write(yaml_output)

# Build indicator categories table
indicator_categories = {
    "id": to_identifier(xlsx_combined, "category"),
    "name": escape(xlsx_combined, "category"),
    "description": "",
    "dimension": to_identifier(xlsx_combined, "dimension")
}
indicator_categories = pd.DataFrame(indicator_categories) \
    .drop_duplicates().reset_index(drop=True) \
    .to_dict(orient='records')

# Write to YAML
yaml_output = yaml.dump(indicator_categories, sort_keys=False, indent=2, allow_unicode=True)
with open(fout_indicator_category_definitions, "w", encoding="utf-8") as f:
    f.write(yaml_output)

# Map datapoints
granularity_mapping = {
    "EveryTwoYears": "EveryTwoYears",
    "Every2Years": "EveryTwoYears",
    "Yearly": "Yearly",
    "EveryYear": "Yearly",
    "Monthly": "Monthly",
    "Weekly": "Weekly",
    "Other": "Other"
}
data_collection_frequencies = []
for tg in xlsx_combined["Frequency of data collection (or dissemniation)"]:
    if isinstance(tg, float):
        data_collection_frequencies.append([])
    else:
        tg = re.sub("[^a-zA-Z0-9]", "", tg.title())
        data_collection_frequencies.append(granularity_mapping.get(tg, "Other"))

# Build the final database structure
databases = {
    "id": to_identifier(xlsx_combined, "Source"),
    "name": xlsx_combined["Source"],
    "author": "",
    "description": "",
    "database_link": xlsx_combined["Link"],
    "update_frequency": data_collection_frequencies,
}
databases = pd.DataFrame(databases).to_dict(orient='records')
# Remove duplicates
databases = list({db['id']:db for db in databases}.values())

# Write to YAML
yaml_output = yaml.dump(databases, sort_keys=False, indent=2, allow_unicode=True)
with open(fout_databases, "w", encoding="utf-8") as f:
    f.write(yaml_output)

# Build the final data collection details structure
data_collection_details = {
    "id": to_identifier(xlsx_combined, "Source") + "_" + to_identifier(xlsx_combined, "Indicator"),
    "name": xlsx_combined["Source"] + "-" + xlsx_combined["Indicator"],
    "description": "",
    "in_database": to_identifier(xlsx_combined, "Source"),
    "measures_indicator": to_identifier(xlsx_combined, "Indicator"),
    "data_link": xlsx_combined["Link"],
    "oldest_datapoint": "",
    "newest_datapoint": xlsx_combined["Latest data availability"],
    "time_granularity": data_collection_frequencies,
    "spatial_granularity": "Country",
    "spatial_scope": "Eu"
}
data_collection_details = pd.DataFrame(data_collection_details).to_dict(orient='records')

# Remove duplicates
data_collection_details = list({dcd['id']:dcd for dcd in data_collection_details}.values())

# Write to YAML
yaml_output = yaml.dump(data_collection_details, sort_keys=False, indent=2, allow_unicode=True)
with open(fout_data_collection_details, "w", encoding="utf-8") as f:
    f.write(yaml_output)
