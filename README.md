# Project Overview

This project implements an ELT pipeline and data transformation process using dbt to build a structured sales data warehouse based on data from the FakeStore API. 
The final output provides a single aggregated table that delivers order level insights, detailing who ordered what and when.

# Project Structure
* `tecovas_dbt_project/`
* `models/`
* `staging/` 
* `sales_marts/`

Note: 
`macros/`  # Custom macros (not used in final implementation)

# dbt

[dbt](https://docs.getdbt.com/docs/introduction) is our tool of choice for transformations within the data warehouse. This repo is responsible for the SQL logic and dbt metadata, which all gets packaged into an image and pushed to ECR.

## Installation

Installation instructions can be found [here](https://docs.getdbt.com/docs/core/installation).

There are several ways of installing dbt, the easiest being to install with pip in a virtual environment:
* `python3 -m venv .env && source .env/bin/activate && pip install -r requirements.txt`
* Verify installation with `dbt --version`

## Local Development

Create `~/.dbt/profiles.yml` with the following:
```yaml
tecovas_dbt_project:
  target: dev
  outputs:
    dev:
      type: postgres
      dbname: tecovas_db
      host: localhost
      port: 5432
      user: <user>
      password: <your_password>
      schema: staging_sales_marts
      threads: 4
```

# Running dbt Locally

Once your dbt environment is set up, you can run the following dbt commands from the project directory locally:
* `dbt deps --project-dir tecovas_dbt_project`
* `dbt build --project-dir tecovas_dbt_project --full-refresh`
* `dbt test --project-dir tecovas_dbt_project`

CLI documentation can be found [here](https://docs.getdbt.com/reference/dbt-commands)

### Upgrading dbt for Local Development
Ensure that your dbt version matches the major/minor version of your dbt adapter (dbt-postgres). If an upgrade is needed, follow these steps:

```sh
source .\venv/bin/activate
pip install --ignore-installed -r requirements.txt
dbt deps --project-dir tecovas_dbt_project
```
If issues persist, you may need to recreate the virtual environment:

```sh
rmdir /s /q venv  # Deletes the existing virtual environment
python -m venv venv  # Recreate the virtual environment
.\venv\Scripts\activate  # Activate the new environment
pip install -r requirements.txt  # Reinstall dependencies
dbt deps --project-dir tecovas_dbt_project
```