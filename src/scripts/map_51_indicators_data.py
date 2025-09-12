import os
import yaml
import pandas as pd

input_files = {
    'economy': 'data/250821_dimension_economy.xlsx',
    'environmental': 'data/250821_dimension_environment.xlsx',
    'health': 'data/250821_dimension_health.xlsx',
    'social': 'data/250821_dimension_society.xlsx',
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

# Map supply chain components
### TODO: CHECK MAPPING
component_mapping = {
    "PrimaryProduction": "PrimaryFoodProduction",
    "Consumption": "FoodConsumption",
    "Retail": "FoodDistribution",
    "Transport": "FoodDistribution",
    "Transport?": "FoodDistribution",
    "Disposal": "FoodProcessing",
    "AllStages": ["PrimaryFoodProduction", "FoodProcessing", "FoodDistribution", "FoodConsumption"]
}
supply_chain_components = []
for lst in xlsx_combined["Related stage of the food supply chain"].str.split(", "):   
    if isinstance(lst, float):
        supply_chain_components.append([])
    else:
        components = [str.title().replace(" ", "") for str in lst]
        components = [component_mapping.get(component, component) for component in components]
        components = list(set(components)) if not isinstance(components[0], list) else components[0]
        supply_chain_components.append(components)

# Build the final indicator data structure
indicator_data = {
    "id": to_identifier(xlsx_combined, "Indicator"),
    "name": xlsx_combined["Indicator"],
    "description": xlsx_combined["Definition"],
    "measurement_unit": xlsx_combined["Unit"],
    "key_area": to_identifier(xlsx_combined, "dimension"),
    "category": to_identifier(xlsx_combined, "category"),
    "supply_chain_component": supply_chain_components,
    "sustainability_impact": xlsx_combined["Impact on sustainability"]
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
