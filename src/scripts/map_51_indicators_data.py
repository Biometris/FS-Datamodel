import yaml
import pandas as pd
import re

input_files = {
    'economy': 'data/250821_dimension_economy.xlsx',
    'environment': 'data/250821_dimension_environment.xlsx',
    'health': 'data/250821_dimension_health.xlsx',
    'society': 'data/250821_dimension_society.xlsx',
}

fout_indicator_definitions = "data/t511_indicators.yaml"
fout_databases = "data/t511_databases.yaml"

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
    return xlsx_combined[column_name].str.title().replace("[^a-zA-Z0-9]", "", regex=True)

# Helper function to create identifiers
def escape(xlsx_combined, column_name):
    return xlsx_combined[column_name].str.title().replace("[“”]", "\"", regex=True)

# Map supply chain components
### TODO: This should ideally be correct in input. Check and throw error?
component_mapping = {
    "Consumption": "Consumption",
    "Connsumption": "Consumption",
    "FoodProcessing": "FoodProcessing",
    "PrimaryProduction": "PrimaryProduction",
    "Retail": "Retail",
    "RetailDistribution": "Retail",
    "Transport": "Transport",
    "DisposalRecycling": "DisposalRecycling"
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
    "measurement_unit": xlsx_combined["Unit"],
    "dimension": to_identifier(xlsx_combined, "dimension"),
    "has_category": to_identifier(xlsx_combined, "category"),
    "supply_chain_component": supply_chain_components,
    "sustainability_impact": xlsx_combined["Impact on sustainability"],
    "granularity": ""
}

# Change data orientation
indicators = pd.DataFrame(indicator_data).to_dict(orient='records')

# Remove missing values.
indicators = [{i:j for i,j in indicator.items() if j == j} for indicator in indicators]

# Write to YAML
yaml_output = yaml.dump(indicators, sort_keys=False, indent=2, allow_unicode=True)
with open(fout_indicator_definitions, "w", encoding="utf-8") as f:
    f.write(yaml_output)

# Build the final indicator data structure
databases = {
    "id": to_identifier(xlsx_combined, "Source"),
    "name": xlsx_combined["Source"]
}
databases = pd.DataFrame(databases).to_dict(orient='records')
databases = list({db['id']:db for db in databases}.values())  # Remove duplicates

# Write to YAML
yaml_output = yaml.dump(databases, sort_keys=False, indent=2, allow_unicode=True)
with open(fout_databases, "w", encoding="utf-8") as f:
    f.write(yaml_output)
