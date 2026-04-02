import os
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from linkml.generators.docgen import DocGenerator, DiagramType

from indicator_datastore import DataStore, DatabaseDataSource

SCHEMA_PATH = "src/schema/food_system_indicators.yaml"

def create_indicator_hierarchy_json(indicators, categories_dict):
    # Output file
    outfile_path_sunburst = "docs/data/indicators_sunburst_chart_data.json"
    outfile_path_tree = "docs/data/indicators_tree_chart_data.json"

    # Build hierarchy
    hierarchy = {}
    for e in indicators:
        if e['outcome_type'] not in hierarchy:
            hierarchy[e['outcome_type']] = {}
        if e['has_category'] not in hierarchy[e['outcome_type']]:
            hierarchy[e['outcome_type']][e['has_category']] = []
        hierarchy[e['outcome_type']][e['has_category']].append(e)

    # Convert hierarchy
    sunburst_data = []
    for outcome_type, categories in hierarchy.items():
        outcome_type_node = {"name": outcome_type, "children": []}
        for category_id, ents in categories.items():
             category_name = categories_dict[category_id]['name']
             category_node = {
                 "name": category_name,
                 "children": [{"name": ent['name'], "value": 1} for ent in ents]
                 }
             outcome_type_node["children"].append(category_node)
        sunburst_data.append(outcome_type_node)

    # Tree data requires base node
    tree_data = {"name": "Indicator hierarchy", "children": sunburst_data}

    # Save JSON for reuse
    Path(outfile_path_sunburst).write_text(json.dumps(sunburst_data, indent=2))
    Path(outfile_path_tree).write_text(json.dumps(tree_data, indent=2))

def create_supply_chain_indicator_hiearchy_json(indicators):
    # Output file
    outfile_path = "docs/data/indicators_supply_chain_chart_data.json"

    # Build hierarchy
    hierarchy = {}
    for e in indicators:
        for s in e['supply_chain_component']:
            if s not in hierarchy:
                hierarchy[s] = []
            hierarchy[s].append(e)

    # Convert hierarchy
    tree_data = {"name": "Supply chain component", "children": []}
    for component, ents in hierarchy.items():
        component_node = {
            "name": component,
            "children": [{"name": ent['name'], "value": 1} for ent in ents]
        }
        tree_data["children"].append(component_node)

    # Save JSON for reuse
    Path(outfile_path).write_text(json.dumps(tree_data, indent=2))

def create_indicator_scores_data_json(criteriascores):

    # Output file
    outfile_path = "docs/data/indicator_scores_chart_data.json"

    score_mapping = {"Strong": 3,
                     "Adequate": 2,
                     "Weak": 1}

    chart_data = []
    for score in criteriascores:
        score_point = [score.get("scores_criterion"),
                       score.get("score_for_indicator"),
                       score_mapping.get(score.get("score"))]
        chart_data.append(score_point)

    # Save JSON for reuse
    Path(outfile_path).write_text(json.dumps(chart_data, indent=2))

def render_template(
    template_name,
    **kwargs
):
    # Out file
    output_file = kwargs.get('output_file') if 'output_file' in kwargs else f"docs/{template_name}.md"

    # Point to templates folder
    env = Environment(loader=FileSystemLoader("./src/docs/templates"))
    template = env.get_template(f"{template_name}.md.j2")

    # Render
    markdown_output = template.render(**kwargs)

    # Save to file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_output)

if __name__ == "__main__":

    # Data sources
    data_sources = [
        DatabaseDataSource("data/indicators.yaml", "Indicator", "Indicators"),
        DatabaseDataSource("data/indicator_categories.yaml", "IndicatorCategory", "IndicatorCategories"),
        DatabaseDataSource("data/indicator_data_collection_details.yaml", "IndicatorDataCollectionDetails", "IndicatorDataCollectionDetails"),
        DatabaseDataSource("data/criteria.yaml", "IndicatorCriterion", "IndicatorCriteria"),
        DatabaseDataSource("data/indicator_scores.yaml", "IndicatorcriteriaScore", "IndicatorCriteriaScores"),
        DatabaseDataSource("data/references.yaml", "Reference", "ReferencesTab"),
        DatabaseDataSource("data/transition_domain_pillars.yaml", "TransitionDomainPillar", "TransitionDomainPillars"),
    ]

    # Setup data store
    datastore = DataStore(
        schema_file=SCHEMA_PATH,
        data_sources=data_sources
    )

    # Exports
    data_export_path = "docs/data"
    glossary_export_path = os.path.join(data_export_path, "glossary.yaml")
    excel_exports = {
        'all': {
            'name': 'All',
            'filename': 'indicator_data_export.xlsx',
            'table_names': None # Set to None to export all
        }
    }

    # Generate model diagram
    doc_gen = DocGenerator(SCHEMA_PATH, importmap={})
    doc_gen.diagram_type = DiagramType.er_diagram
    diagram_classes = [
        'Indicator',
        'IndicatorCategory',        
        'IndicatorDataCollectionDetails',
        'IndicatorDatapoint',
        'IndicatorCriterion',
        'IndicatorcriteriaScore',
        'Reference'
    ]   

    # Validate database content.
    if datastore.validate_data():

        # Get indicators and create hierarchy JSON and table
        indicator_categories = datastore.get_indicator_categories()
        indicator_categories_dict = res = {i['id']: i for i in indicator_categories}
        references = datastore.get_references()
        references_dict = res = {r['id']: r for r in references}
        indicators = datastore.get_indicators()
        indicators_dict = res = {i['id']: i for i in indicators}
        databases = datastore.get_databases()
        databases_dict = res = {d['id']: d for d in databases}
        indicator_data_collection_details = datastore.get_indicator_indicator_data_collection_details()
        database_indicators = {}
        for record in indicator_data_collection_details:
            database_indicators.setdefault(record['in_database'], []).append(record)

        enum_dict = datastore.create_enum_dict()
        create_indicator_hierarchy_json(indicators, indicator_categories_dict)
        create_supply_chain_indicator_hiearchy_json(indicators)

        render_template(
            template_name = 'indicators',
            indicators = indicators,
            categories_dict = indicator_categories_dict,
            enum_dict = enum_dict
        )

        render_template(
            template_name = 'indicator_categories',
            categories = indicator_categories,
            sources_dict = references_dict,
            enum_dict = enum_dict
        )        

        for indicator in indicators:
            render_template(
                template_name = 'indicator_details',
                output_file = f"docs/indicators/{indicator['id']}.md",
                indicator = indicator,
                enum_dict = enum_dict
            )

        render_template(
            template_name = 'databases_table',
            databases = databases
        )

        for database in databases:
            render_template(
                template_name = 'database_details',
                output_file = f"docs/databases/{database['id']}.md",
                database = database,
                database_indicators = database_indicators[database['id']] if database['id'] in database_indicators.keys() else [],
                indicators_dict = indicators_dict,
                enum_dict = enum_dict
            )

        render_template(
            template_name = 'indicator_data_collection_details_table',
            indicators_dict = indicators_dict,
            databases_dict = databases_dict,
            indicator_data_collection_details = indicator_data_collection_details
        )

        for collection in indicator_data_collection_details:
            render_template(
                template_name = 'indicator_data_collection_details',
                output_file = f"docs/indicator_data_collection_details/{collection['id']}.md",
                collection = collection,
                indicator = indicators_dict[collection['measures_indicator']],
                database = databases_dict[collection['in_database']],
                enum_dict = enum_dict
            )
                
        criteria = datastore.get_indicator_criteria()
        render_template(
            template_name = 'indicator_criteria',
            criteria = criteria,
            enum_dict = enum_dict
        )

        render_template(
            template_name = 'indicator_criteria_rationale',
            criteria = criteria,
            enum_dict = enum_dict
        )

        criteria_scores = datastore.get_indicator_criteria_scores(
            include_missing = True,
            indicators = indicators,
            criteria = criteria,
            output_path = os.path.join(data_export_path, 'indicator_scores.xlsx')
        )
        create_indicator_scores_data_json(criteria_scores)
        render_template(
            template_name = 'indicator_scores'
        )

        render_template(
            template_name = 'references',
            sources = references,
            enum_dict = enum_dict
        )

        # Export glossary terms
        datastore.export_glossary_yaml(glossary_export_path)

        # Create data exports
        for key, excel_export in excel_exports.items():
            print(f'Exporting {key}')
            full_path = os.path.join(data_export_path, excel_export['filename'])
            datastore.export_to_excel(
                full_path,
                table_names = excel_export['table_names']
            )

