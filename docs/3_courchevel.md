# Initializing a database with test fixtures

## Purpose

I wanted to document the steps necessary to take a vanilla database image and customize the data loaded into the container at runtime. This information is also captured in a working example [here](../courchevel). The Docker image is available [here](https://hub.docker.com/r/mwprcvl/courchevel).

## Prerequisites

The following text assumes Docker is installed and familiarity with `docker-compose`.

## Creating a `docker-compose.yml` configuration file

I start out with a basic `Dockerfile`.

```docker
ARG base_tag=11.2-alpine
FROM postgres:${base_tag}
```

To launch the container the minimum requirement is a database, a user, and a password, through environment variables that the base image understands. I also specify a host port. Environment variables that are used by compose are in a `.env` file. Environment variables used by the container are in an `env_file`, the name of which is specified in `.env`.

```yml
version: '3.6'
services:
  db:
    build:
      args:
        base_tag: 11.2-alpine
      context: .
    env_file:
      - ${ENV_FILE}
    environment:
      - POSTGRES_USER=courchevel
      - POSTGRES_PASSWORD=courchevel
      - POSTGRES_DB=courchevel
    image: courchevel:latest
    ports:
      -
        published: ${POSTGRES_HOST_PORT}
        target: 5432
```

I can then run `docker-compose up -d` and connect to the database, using the credential defined in the YAML file.

```sh
psql -h <docker_ip> -p ${POSTGRES_HOST_PORT} -U courchevel
```

## Initializing the database with test fixtures

I want to be able to share a database image that will automatically load resources, for example for testing. The Postgres image has an entrypoint that will do this. The entrypoint looks for scripts in the `/docker-entrypoint-initdb.d` directory, and runs them in ASCII order. The Dockerfile needs a `COPY` instruction.

Option 1 uses an `ENV` instruction to say where the scripts are. I would use this if the scripts were coming from somewhere that I had control over. The variable assigned to `ENV` could be hard coded or come from an `env_file`.

```docker
ENV init_scripts_path=db_init
COPY ${init_scripts_path} /docker-entrypoint-initdb.d/
```

I use an `ARG` instruction to say where the scripts are.

```docker
ARG init_scripts_path=db_init_default
COPY ${init_scripts_path} /docker-entrypoint-initdb.d/
```

The YAML config contains the reference to the build argument.

```yml
services:
  db:
    build:
      args:
        init_scripts_path: ${DB_INIT_SCRIPTS_PATH}
```

The variable assigned by the `ARG` instruction could be hard coded or come from a `.env` file.

```docker
DB_INIT_SCRIPTS_PATH=db_init_alternate
```

Within `./db_init` I have a file, `10_create_table.sql` which contains a simple create statement:

```sql
CREATE TABLE web_origins (
    client_id character varying(36) NOT NULL,
    value character varying(255)
);
```

When the container is launched, the output should look something like the following:

```txt
database_1  | 2019-02-16 22:06:33.351 UTC [31] LOG:  database system is ready to accept connections
database_1  |  done
database_1  | server started
database_1  | CREATE DATABASE
database_1  | /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/10_create_table.sql
database_1  | CREATE TABLE
database_1  | waiting for server to shut down....2019-02-16 22:06:34.093 UTC [31] LOG:  received fast shutdown request
```

## Using an environment variable in a test fixture

Sometimes I want to specify a variable on the host to be used by the container's SQL script. The Postgres image entrypoint also execute shell scripts, which in turn can use environment variables.

The shell script, in `./db_init`, builds a SQL statement then executes it using `psql`.

```bash
#!/usr/bin/env bash
set -ex

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE ROLE $DUMMY_ROLE;
EOSQL
```

Upon container launch, the variable `DUMMY_USER` from my envfile `dev.env` are substituted and the role is created.

There is a nice writeup of a more involved shell script using enviroment variables [here](https://medium.com/@beld_pro/quick-tip-creating-a-postgresql-container-with-default-user-and-password-8bb2adb82342).

## Persisting the state of the database

Sometimes the initialization scripts may take along time. In this case, we do not want to wait for them to run every time we want a new container. A solution here is to use a `VOLUME` instruction so that the initial state of the database is persisted on the host and can be reused by another container.

```yml
services:
  db:
    volumes:
      -
        type: bind
        source: ./db_data
        target: /var/lib/postgresql/data
```

I had a nasty surprise when I tried this method out on a much older Mac, and I found that I could not use a source directory with a `bind`. Instead, I needed to use a `docker volume`.

```yml
services:
  db:
    volumes:
      -
        type: volume
        source: db_1
        target: /var/lib/postgresql/data
volumes:
  db_1:
```

## Launching a second container with the scripts already loaded

Another option for decreasing boot time if the initialization scripts are long running is to use of copy of the volume used by the database. First I tag the image to use for clarity.

```sh
docker tag courchevel:latest courchevel:postinit
```

A second compose file points to the image I just tagged, using a source volume that will contain a copy of the volume created by the initialization that the first container run performed.

```yml
version: '3.6'
services:
  db:
    env_file:
      - ${ENV_FILE}
    image: courchevel:postinit
    ports:
      -
        published: ${POSTINIT_POSTGRES_HOST_PORT}
        target: 5432
    volumes:
      -
        type: bind
        source: ./db_data_postinit
        target: /var/lib/postgresql/data
```

For the older Mac, I changed the volume declaration to be consistent with my first YAML file, but instead using `db_2`, which I will create later.

I copy the volume from the first container to make it available to the second without modifying the original copy; this is so that I can restart quickly if I make breaking changes to the data. The second container is now launched using the alternate compose file, and an alternate project name to avoid a namespace collision with the first container. I capture this in `postinit_up.sh`.

```sh
rm -r ./db_data_postinit
mkdir -p ./db_data_postinit
cp -r ./db_data/* ./db_data_postinit
```

Again, for the older Mac this script is replaced with one that copies the `docker volume`, `courchevel_db_1`, into `courchevelpostinit_db_1`. Script from [here](https://github.com/gdiepen/docker-convenience-scripts)

```sh
bash docker_volume_clone.sh courchevel_db_1 courchevelpostinit_db_1
```

In either case, the container using the cloned or copied Docker volume can now be started.

```sh
docker-compose -f docker-compose-postinit.yml -p courchevelpostinit_db_1 down
```

This 'postinit' container is also stopped using the options above.

```sh
docker-compose -f docker-compose-init.yml -p courchevelpostinit down
```

## Summary

I have demonstrated the use of initialization scripts to load data into Postgres upon container launch. I have shown how to incorporate environment variables into the initialization SQL scripts. I have also shown two ways to persist data for a containerized database.
