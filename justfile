# Load environment variables from config.public.mk or specified file
set dotenv-load := true

# set dotenv-filename := env_var_or_default("LINKML_ENVIRONMENT_FILENAME", "config.public.mk")
set dotenv-filename := x'${LINKML_ENVIRONMENT_FILENAME:-config.public.mk}'

# List all commands as default command. The prefix "_" hides the command.
_default: _status
    @just --list

# Set cross-platform Python shebang line (assumes presence of launcher on Windows)
shebang := if os() == 'windows' {
  'py'
} else {
  '/usr/bin/env python3'
}

# Environment variables with defaults
schema_name := env_var_or_default("LINKML_SCHEMA_NAME", "")
source_schema_path := env_var_or_default("LINKML_SCHEMA_SOURCE_PATH", "")

config_yaml := if env_var_or_default("LINKML_GENERATORS_CONFIG_YAML", "") != "" {
  "--config-file " + env_var_or_default("LINKML_GENERATORS_CONFIG_YAML", "")
} else {
  ""
}
gen_doc_args := env_var_or_default("LINKML_GENERATORS_DOC_ARGS", "")
gen_owl_args := env_var_or_default("LINKML_GENERATORS_OWL_ARGS", "")
gen_java_args := env_var_or_default("LINKML_GENERATORS_JAVA_ARGS", "")
gen_ts_args := env_var_or_default("LINKML_GENERATORS_TYPESCRIPT_ARGS", "")

# Directory variables
src := "src"
dest := "project"
docdir := "docs"
templatedir := src / "docs" / "templates"
exampledir := "examples"
datadir := "data"

# Show current project status
_status: _check-config
    @echo "Project: {{schema_name}}"
    @echo "Source: {{source_schema_path}}"

# Check project configuration
_check-config:
    #!{{shebang}}
    import os
    schema_name = os.getenv('LINKML_SCHEMA_NAME')
    if not schema_name:
        print('**Project not configured**:\n - See \'.env.public\'')
        exit(1)
    print('Project-status: Ok')

# Generate all project files
alias all := site

# Generate site locally
site: clean _gen-project _gendoc

# Clean all generated files
clean:
    rm -rf {{dest}}
    rm -rf tmp
    rm -rf {{docdir}}/*

# Generate project files
_gen-project:    
    gen-project {{config_yaml}} -d {{dest}} {{source_schema_path}}
    @if [ ! -z "${{gen_owl_args}}" ]; then \
      mkdir -p {{dest}}/owl || true && \
      gen-owl {{gen_owl_args}} {{source_schema_path}} > {{dest}}/owl/{{schema_name}}.owl.ttl || true ; \
    fi
    @if [ ! ${{gen_java_args}} ]; then \
      gen-java {{gen_java_args}} --output-directory {{dest}}/java/ {{source_schema_path}} || true ; \
    fi
    @if [ ! ${{gen_ts_args}} ]; then \
      gen-typescript {{gen_ts_args}} {{source_schema_path}} > {{dest}}/typescript/{{schema_name}}.ts || true ; \
    fi

# Generate documentation
_gendoc: _ensure_docdir _gen_viz _gen_er _gen_exampledata
    # DO NOT REMOVE: these cp statements are crucial to maintain the w3 ids for the model artifacts
    cp {{dest}}/owl/{{schema_name}}.owl.ttl {{docdir}}/{{schema_name}}.owl.ttl ; \
    cp {{dest}}/jsonld/{{schema_name}}.context.jsonld {{docdir}}/{{schema_name}}.context.jsonld ; \
    cp {{dest}}/jsonld/{{schema_name}}.context.jsonld {{docdir}}/context.jsonld ; \
    cp {{dest}}/jsonld/{{schema_name}}.jsonld {{docdir}}/{{schema_name}}.jsonld ; \
    cp {{dest}}/jsonschema/{{schema_name}}.schema.json {{docdir}}/{{schema_name}}.json ; \
    cp {{dest}}/graphql/{{schema_name}}.graphql {{docdir}}/{{schema_name}}.graphql ; \
    cp {{dest}}/shex/{{schema_name}}.shex {{docdir}}/{{schema_name}}n.shex ; \
    cp {{dest}}/shacl/{{schema_name}}.shacl.ttl {{docdir}}/{{schema_name}}.shacl.ttl ; \
    cp {{dest}}/prefixmap/* {{docdir}} ; \

    cp -r {{src}}/docs/files/* {{docdir}}
    gen-doc {{gen_doc_args}} -d {{docdir}} --template-directory {{templatedir}} {{source_schema_path}}    

# Generate er diagram
_gen_er:
  gen-erdiagram {{source_schema_path}} > {{docdir}}/erdiagram.md

# Generate plantuml diagram
_gen_plantuml:
  gen-plantuml {{source_schema_path}} --directory {{docdir}}  

# Generate example data table
_gen_exampledata:
  {{shebang}} {{src}}/scripts/generate_exampledata.py 

_gen_viz:
    {{shebang}} {{src}}/scripts/generate_json.py

_ensure_docdir:
    -mkdir -p {{docdir}}

_ensure_examples_output:
    -mkdir -p examples/output

# Test documentation locally
testdoc: _gendoc serve

serve:
  - mkdocs serve

mkdocs:
  mkdocs
