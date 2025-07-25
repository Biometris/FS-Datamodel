# config.public.mk

# This file is public in git. No sensitive info allowed.
# These variables are sourced in Makefile, following make-file conventions.
# Be aware that this file does not follow python or bash conventions, so may appear a little unfamiliar.

###### schema definition variables, used by makefile

# Note: makefile variables should not be quoted, as makefile handles quoting differently than bash
LINKML_SCHEMA_NAME="food_system_indicators"
LINKML_SCHEMA_AUTHOR="Bart-Jan van Rossum <bart-jan.vanrossum@wur.nl>"
LINKML_SCHEMA_DESCRIPTION="This is the project description."
LINKML_SCHEMA_SOURCE_PATH="src/schema/food_system_indicators.yaml"

###### linkml generator variables, used by makefile

## gen-project configuration file
LINKML_GENERATORS_CONFIG_YAML=config.yaml

## pass args if gendoc ignores config.yaml (i.e. --no-mergeimports)
# LINKML_GENERATORS_DOC_ARGS="--diagram-type plantuml_class_diagram --include-top-level-diagram"
# LINKML_GENERATORS_DOC_ARGS="--diagram-type mermaid_class_diagram --include-top-level-diagram"
LINKML_GENERATORS_DOC_ARGS="--diagram-type er_diagram --include-top-level-diagram"

## pass args to workaround genowl rdfs config bug (linkml#1453)
##   (i.e. --no-type-objects --no-metaclasses --metadata-profile rdfs)
LINKML_GENERATORS_OWL_ARGS=

## pass args to trigger experimental java/typescript generation
LINKML_GENERATORS_JAVA_ARGS=
LINKML_GENERATORS_TYPESCRIPT_ARGS=
