# FutureFoods sustainable food systems indicators data model

This repository builds a LinkML-based food system indicators model, generates documentation, and publishes the site to GitHub Pages.

## Repository structure

- `src/schema/` contains the LinkML schema definition and related configuration files for the data model.
- `data/` holds the YAML source data used to describe indicators, scores, categories, and references.
- `project/` contains generated model artifacts such as JSON Schema, JSON-LD, SHACL, and other downstream formats.
- `docs/` contains the documentation source and generated site content used by MkDocs.
- `src/scripts/` contains helper scripts for converting and preparing data for the docs and website.

## Prerequisites

- Python 3.13+
- `just` installed on your system
- Internet access to install Python packages

## Setup

Create and activate a virtual environment, then install the required Python packages:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash / WSL
# or: .\.venv\Scripts\Activate.ps1  # PowerShell
pip install -r requirements.txt
```

The build uses the configuration in `config.public.mk` and the schema source in `src/schema/food_system_indicators.yaml`.

## Build the LinkML model

Generate the project artifacts and documentation:

```bash
just site
```

This runs the full build pipeline, including cleaning old output, generating the LinkML project files, creating documentation, and converting the indicator data views.

## Run the additional scripts

Useful helper commands:

```bash
just convert   # convert YAML indicator data to the JSON views used by the docs
just validate  # validate the data against the schema
just serve     # start the local MkDocs site
```

## Build and publish the docs

To build the documentation locally:

```bash
just site
just serve
```
