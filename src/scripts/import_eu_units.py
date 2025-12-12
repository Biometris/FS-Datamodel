import os
import csv
import yaml
import urllib
import urllib.request

ENUM_NAME = "IndicatorMeasurementUnit"
ENUM_TITLE = "Eurostat unit of measurement"
ENUM_DESCRIPTION = "Food system indicator units of measurement imported from the Eurostat unit of measure dictionary/vocabulary."
CURIE_PREFIX = 'euunit'
ENUM_SEE_ALSO = 'https://dd.eionet.europa.eu/vocabulary/eurostat/unit/view'
URL_PREFIX = 'http://dd.eionet.europa.eu/vocabulary/eurostat/unit/'
EUROSTAT_UNIT_VOCAB_URL = 'https://dd.eionet.europa.eu/vocabulary/eurostat/unit/csv'
EUROSTAT_UNIT_CSV_PATH = "./data/eurostat-unit-enums.csv"
EUROSTAT_UNIT_YAML_PATH = "./src/schema/eurostat-unit-enums.yaml"

def csv_to_linkml_enum(csv_path):
    enum = {
        "id": "fsi_eu_units_schema",
        "name": "fsi_eu_units_schema",
        "description": "LinkML schema food system indicator units (imported from the Eurostat unit of measurement vocabulary).",
        "see_also": [ ENUM_SEE_ALSO ],
        "enums": {
            ENUM_NAME: {
                "title": ENUM_TITLE,
                "description": ENUM_DESCRIPTION,
                "permissible_values": {}
            }
        }
    }

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            notation = row["Notation"]
            if not notation:
                continue
            
            id = notation.replace("-", "_")
            label = row["Label"] or notation
            definition = row["Definition"] or None
            
            pv = {"title": label}
            if definition:
                pv["description"] = definition
            else:
                pv["description"] = label

            pv["meaning"] = f"{CURIE_PREFIX}:{notation}"
            
            enum["enums"][ENUM_NAME]["permissible_values"][id] = pv

    return enum

def get_eurostat_unit_csv(url=EUROSTAT_UNIT_VOCAB_URL, filepath=EUROSTAT_UNIT_CSV_PATH):
    # download only if the file does not already exist
    if not os.path.exists(filepath):
        print(f"Downloading Eurostat units CSV to {filepath}")
        urllib.request.urlretrieve(url, filepath)
    else:
        print(f"Using cached CSV from {filepath}")

get_eurostat_unit_csv()
enums = csv_to_linkml_enum(EUROSTAT_UNIT_CSV_PATH)

enums_yaml = yaml.dump(enums, sort_keys=False, allow_unicode=True)
with open(EUROSTAT_UNIT_YAML_PATH, "w", encoding="utf-8") as f:
    f.write(enums_yaml)

os.remove(EUROSTAT_UNIT_CSV_PATH)
