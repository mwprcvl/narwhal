# A simple python service with a database container

## Purpose

Document the steps involved in setting up containers containing a Python development environment and a PostgreSQL database. This information is also captured in a working example [here](../pipyan). The Docker images for each container are available for [PostgreSQL](https://hub.docker.com/r/mwprcvl/pipyan_db), and [Python](https://hub.docker.com/r/mwprcvl/pipyan_py).

## Prerequisites

Docker installed. VSCode installed for debugging. Awareness of the previous notes on Docker, (here)[..]

## Project outline

I organize the project to house orchestration files (`Makefile`, `docker-compose.yml`) at the top level, with one subdirectory for each service, each of which contains a `Dockerfile` for the service. The compose file reflects this structure. Relative paths in the compose file are from the directory that the compose file is called from, for example the build context for each image.

```yml
version: "3.6"
services:
  db:
    build:
      ...
      context: ./db/
  ...
  py:
    build:
      ...
      context: ./py/
    ...
```

Also at the top level, a `.env` file contains all environment variables used by compose.

```sh
PROJECT=pipyan
ENV_FILE=dev.env
POSTGRES_DB_HOST=db
POSTGRES_DB_PORT=5432
DB_INIT_SCRIPTS_PATH=db_init
DB_POSTGRES_HOST_PORT=15432
PY_AIRFLOW_HOME=/airflow
PY_DAGS_PATH=/airflow/dags
PY_DATA_PATH=/data
PY_PYTHONPATH=/app
PY_AIRFLOW_PORT=18080
PY_DASH_PORT=18050
PY_DEBUG_PORT=13000
PY_FLASK_PORT=15000
```

## Summary

I have demonstrated how to configure a PostgreSQL database container with Python including Airflow, Dash, and Flask.
