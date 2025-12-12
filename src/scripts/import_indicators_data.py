import yaml
import csv
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

# Helper function to get unit mappings
def build_unit_mapping(csv_path):
    mapping = {}
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            orig = row["Orig"].strip()
            eu_units_raw = row["EU_Unit"].strip()
            units = [u.strip() for u in eu_units_raw.split(";") if u.strip()]
            mapping[orig] = units
    return mapping

# Helper field to remove empty fields 
def skip_empty_field(records, field):
    for row in records:
        v = row.get(field)
        if v is None or v == "" or (isinstance(v, float) and pd.isna(v)):
            row.pop(field, None)
    return records

# Helper function to create identifiers
def to_identifier(xlsx_combined, column_name):
    result = xlsx_combined[column_name] \
        .str.title().replace("[^a-zA-Z0-9]", "", regex=True) \
        .str.slice(0, 50)
    return result

# Create mapping from original indicator names to FSI indicator codes
indicator_code_map = {}
fsi_identifiers = to_identifier(xlsx_combined, "Indicator")
for idx, record in fsi_identifiers.items():
    code = record
    indicator_code_map[code] = f"FSI_{idx:04d}"

# Helper function to create food system indicator identifiers
def to_fsi_identifier(xlsx_combined, column_name):
    records = to_identifier(xlsx_combined, column_name)
    result = []
    for record in records:
        result.append(indicator_code_map[record])
    return result

# Helper function to create identifiers
def escape(xlsx_combined, column_name):
    return xlsx_combined[column_name] \
        .str.replace("[\u201C\u201D]", "\"", regex=True) \
        .str.replace("\u00d7", "x", regex=True) \
        .str.replace("\u2013", "-", regex=True) \
        .str.replace("\u2018", "'", regex=True) \
        .str.replace("\u2019", "'", regex=True) \
        .str.replace("\n", " ", regex=True)

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

# Build unit mappings
csv_file = "data/measurement_unit_mappings.csv"
units_mapping = build_unit_mapping(csv_file)
measurement_units = []
for record in xlsx_combined["Unit"]:
    units = units_mapping.get(record.strip(), None)
    if units:
        units = list(set(units)) if not isinstance(units[0], list) else units[0]
        units.sort()
        measurement_units.append(units)
    else:
        measurement_units.append([])

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
        components.sort()
        supply_chain_components.append(components)

# Map EU SDG indicator codes
eu_sdg_indicator_mappings = {
    "FSI_0000": "EU_SDG_02_20",
    "FSI_0006": "EU_SDG_02_30",
    "FSI_0007": "EU_SDG_08_10",
    "FSI_0029": "EU_SDG_15_50",
    "FSI_0030": "EU_SDG_06_60",
    "FSI_0042": "EU_SDG_02_40",
    "FSI_0052": "EU_SDG_02_60",
    "FSI_0064": "EU_SDG_02_53",
    "FSI_0076": "EU_SDG_15_42",
    "FSI_0103": "EU_SDG_02_10",
    "FSI_0137": "EU_SDG_06_40",
    "FSI_0172": "EU_SDG_01_40",
    "FSI_0173": "EU_SDG_08_30",
    "FSI_0177": "EU_SDG_01_10",
    "FSI_0179": "EU_SDG_01_10a"
}
eu_sdg_indicator_codes = []
for idx, record in fsi_identifiers.items():
    code = indicator_code_map[record]
    eu_sdg_indicator_codes.append(eu_sdg_indicator_mappings.get(code, ''))

# Build the final indicator data structure
indicator_data = {
    "id": to_fsi_identifier(xlsx_combined, "Indicator"),
    "name": escape(xlsx_combined, "Indicator"),
    "description": escape(xlsx_combined, "Definition"),
    "definition": "",
    "eu2025_sdg_indicator_code": eu_sdg_indicator_codes,
    "measurement_unit_description": xlsx_combined["Unit"],
    "measurement_units": measurement_units,
    "dimension": to_identifier(xlsx_combined, "dimension"),
    "has_category": to_identifier(xlsx_combined, "category"),
    "supply_chain_component": supply_chain_components,
    "sustainability_impact": map_sustainability_impact(xlsx_combined, "Impact on sustainability")
}

# Change data orientation
indicators = pd.DataFrame(indicator_data).to_dict(orient='records')

# Remove missing values.
indicators = [{i:j for i,j in indicator.items() if j == j} for indicator in indicators]

# Remove undefined SDG indicator codes
indicators = skip_empty_field(indicators, "eu2025_sdg_indicator_code")

# Write to YAML
yaml_output = yaml.dump(indicators, sort_keys=False, indent=2, allow_unicode=True, width=float("inf"))
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
yaml_output = yaml.dump(indicator_categories, sort_keys=False, indent=2, allow_unicode=True, width=float("inf"))
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
yaml_output = yaml.dump(databases, sort_keys=False, indent=2, allow_unicode=True, width=float("inf"))
with open(fout_databases, "w", encoding="utf-8") as f:
    f.write(yaml_output)

# Build the final data collection details structure
data_collection_details = {
    "id": to_identifier(xlsx_combined, "Source") + "_" + to_identifier(xlsx_combined, "Indicator"),
    "name": xlsx_combined["Source"] + "-" + xlsx_combined["Indicator"],
    "description": "",
    "in_database": to_identifier(xlsx_combined, "Source"),
    "measures_indicator": to_fsi_identifier(xlsx_combined, "Indicator"),
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
yaml_output = yaml.dump(data_collection_details, sort_keys=False, indent=2, allow_unicode=True, width=float("inf"))
with open(fout_data_collection_details, "w", encoding="utf-8") as f:
    f.write(yaml_output)
