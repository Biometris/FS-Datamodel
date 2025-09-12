from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader

from indicator_datastore import DataStore

def create_indicator_hiearchy_json(indicators):
    # Output file
    outfile_path_sunburst = "docs/data/indicators_sunburst_chart_data.json"
    outfile_path_tree = "docs/data/indicators_tree_chart_data.json"

    # Build hierarchy
    hierarchy = {}
    for e in indicators:
        if e['key_area'] not in hierarchy:
            hierarchy[e['key_area']] = {}
        if e['thematic_area'] not in hierarchy[e['key_area']]:
            hierarchy[e['key_area']][e['thematic_area']] = {}
        if e['indicator_domain'] not in hierarchy[e['key_area']][e['thematic_area']]:
            hierarchy[e['key_area']][e['thematic_area']][e['indicator_domain']] = []
        hierarchy[e['key_area']][e['thematic_area']][e['indicator_domain']].append(e)
       
    # Convert hierarchy
    sunburst_data = []
    for key_area, thematic_groups in hierarchy.items():
        key_area_node = {"name": key_area, "children": []}
        for thematic_area_id, domain_groups in thematic_groups.items():
            thematic_node = {
                "name": thematic_area_id, 
                "children": []
            }
            for domain_group_id, ents in domain_groups.items():
                domain_node = {
                    "name": domain_group_id,
                    "children": [{"name": ent['name'], "value": 1} for ent in ents]
                }
                thematic_node["children"].append(domain_node)
            
            key_area_node["children"].append(thematic_node)
        sunburst_data.append(key_area_node)

    # Tree data requires base node
    tree_data = {"name": "JRC hierarchy", "children": sunburst_data}

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

def render_template(
    template_name,
    **kwargs
):
    # Out file
    output_file = f"docs/{template_name}.md"

    # Point to templates folder
    env = Environment(loader=FileSystemLoader("./src/docs/templates"))
    template = env.get_template(f"{template_name}.md.j2")

    # Render
    markdown_output = template.render(**kwargs)

    # Save to file
    with open(output_file, "w") as f:
        f.write(markdown_output)

if __name__ == "__main__":
    schema_path = "src/schema/food_system_indicators.yaml"
    indicator_data_path = "data/indicators.yaml"
    database_data_path = "data/databases.yaml"
    datasource_data_path = "data/datasources.yaml"
    criterion_data_path = "data/criteria.yaml"

    # Setup data store
    datastore = DataStore(
        schema_file=schema_path,
        indicators_file=indicator_data_path,
        databases_file=database_data_path,
        datasources_file=datasource_data_path,
        criteria_file=criterion_data_path
    )

    # Validate database content.
    if datastore.validate_data():

        # Get indicators and create hierarchy JSON and table
        indicators = datastore.get_indicators()
        create_indicator_hiearchy_json(indicators)
        create_supply_chain_indicator_hiearchy_json(indicators)

        render_template(
            template_name = 'indicators_table',
            indicators = indicators
        )

        # Get database and create output table.
        databases = datastore.get_databases()
        render_template(
            template_name = 'databases_table',
            databases = databases
        )

        datasources = datastore.get_indicator_datasources()
        render_template(
            template_name = 'indicator_datasources_table',
            datasources = datasources
        )

        criteria = datastore.get_indicator_criteria()
        render_template(
            template_name = 'indicator_criteria_table',
            criteria = criteria
        )

        domains = datastore.get_domains()
        render_template(
            template_name = 'domains_table',
            domains = domains
        )


