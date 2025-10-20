from linkml_runtime import SchemaView
from linkml_store import Client
from linkml_store.utils.format_utils import load_objects
from linkml_store.api.queries import Query

class DataStore:
    def __init__(
        self,
        schema_file: str,
        indicators_file: str,
        databases_file: str,
        datasources_file: str,
        criteria_file: str,
        indicatorscores_file: str
    ):
        # Initialize LinkML Store with DuckDB
        self.client = Client()
        self.db = self.client.attach_database("duckdb", alias="mydb", recreate_if_exists=True)

        # Load schema
        sv = SchemaView(schema_file)
        self.db.set_schema_view(sv)

        # Add database data from yaml to db.             
        self.add_database_data(indicators_file, "Indicator", "Indicators")        
        self.add_database_data(datasources_file, "IndicatorDataSource", "IndicatorDataSources")
        self.add_database_data(databases_file, "Database", "Databases")
        self.add_database_data(criteria_file, "IndicatorCriterion", "IndicatorCriteria")
        self.add_database_data(indicatorscores_file, "IndicatorcriteriaScore", "IndicatorCriteriaScores")

        # Validate cross-links
        print("\nRunning validation...")
        self.validate_data()

    # Add data collection to database.
    def add_database_data(
        self,
        data_path,
        reference_class,
        collection_name
    ):
        collection = self.db.create_collection(reference_class, collection_name)
        objects = load_objects(data_path)        

        collection.insert(objects)

    def validate_data(self):
        valid = True

        # Validate each collection
        collections = self.db.list_collections()
        for c in collections:
            for r in c.iter_validate_collection():
                valid = False
                print(r.message)

        # Validate cross-references between Databases and IndicatorDataSources
        database_collection = self.db.get_collection("Databases")
        data_source_collection = self.db.get_collection("IndicatorDataSources")
        for database in database_collection.rows_iter():
            data_sources = database.get("contains_indicator_data_source")
            for data_source in data_sources:
                if data_source is not None and len(data_source_collection.find({"id": data_source}).rows) == 0:
                    print(data_source + " specified in database " + database.get("id") + " is not in the collection of datasources.")
                    valid = False

        # Validate cross-references between Indicators and IndicatorDataSources
        indicator_collection = self.db.get_collection("Indicators")
        data_source_collection = self.db.get_collection("IndicatorDataSources")        
        for data_source in data_source_collection.rows_iter():            
            indicator = data_source.get("measures_indicator")            
            if indicator is not None and len(indicator_collection.find({"id": indicator}).rows) == 0:
                print(indicator + " specified in data source " + data_source.get("id") + " is not in the collection of indicators.")
                valid = False

        return valid
    
    def create_enum_dict(self):
        view = self.db.schema_view

        enum_dict = {}
        for e in view.all_enums():
            enum = self.db.schema_view.get_enum(e)
            permissible_values = enum.permissible_values
            enum_dict[enum.name] = {
                pv: (permissible_values[pv].title if permissible_values[pv].title else permissible_values[pv].description) for pv in permissible_values
            }

        for s in view.all_slots():
            slot = self.db.schema_view.get_element(s)
            any_of = getattr(slot, "any_of")
            if any_of:
                full_range = {}
                for r in any_of:
                    full_range = dict(enum_dict[getattr(r, "range")], **full_range)
                enum_dict[getattr(slot, "range")] = full_range
        
        return(enum_dict)

    def get_indicators(self):
        """Return a joined view of indicators"""
        q = Query(from_table="Indicators", limit=1000)
        return self.db.query(q).rows

    def get_databases(self):
        """Return a joined view of databases"""
        q = Query(from_table="Databases", limit=1000)
        return self.db.query(q).rows

    def get_indicator_datasources(self):
        """Return a joined view of indicator data sources"""
        q = Query(from_table="IndicatorDataSources", limit=1000)
        return self.db.query(q).rows

    def get_indicator_criteria(self):
        """Return a joined view of indicator criteria"""
        q = Query(from_table="IndicatorCriteria", limit=1000)
        return self.db.query(q).rows
    
    def get_indicator_criteria_scores(self):
        """Return a joined view of indicator criteria scores"""
        q = Query(from_table="IndicatorCriteriaScores", limit=1000)
        return self.db.query(q).rows
    
    def get_domains(self):
        """Return a joined view of indicator domains"""
        q = Query(from_table="Indicators",
                  select_cols=["key_area", "thematic_area", "indicator_domain"])
        
        domains = [dict(s) for s in set(frozenset(d.items()) for d in self.db.query(q).rows)]
        sorted_domains = sorted(domains, key=lambda i: (i["key_area"], i["thematic_area"], i["indicator_domain"]))
                        
        return sorted_domains
    
