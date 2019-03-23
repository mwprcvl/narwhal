# Getting started with Compose

## Purpose

I wanted to document some of the things I have leared about `docker-compose`, henceforth referred to as Compose, particularly multiple containers and the nuances of using environment variables from various sources. This information is also captured in a working example [here](../lesarcs).

## Prerequisites

The following text assumes Docker is installed and familiarity with `docker build` and `docker run`.

## Basic operations

Put configuration into a YAML file, usually `docker-compose.yml`. This file takes care of many of the options that would have had to be passed to `docker build` and `docker run`.

Use compose to bring up services in a detached state.

```sh
docker-compose up -d
```

Use compose to bring down the services.

```sh
docker-compose down
```

## Creating a Compose configuration file

Now we should understand the anatomy of the `docker-compose.yml` file and what each instruction does.

First, top level keys. The top level key `version` simply says which version of `compose` YAML to use. The top level key `services` harbors each service that the service requires. Configuration of many services is thus performed in a single YAML file. In this example I will set up a `database` container along with an `app` container

```yml
version: '3.6'
services:
  database: ...
  app: ...
```

For the `database` container, the environment is defined under `environment` in the YAML, or under an `env_file` referenced in the YAML, or in a `.env` file. A pattern I have used is to use `.env` to specify which `env_file` to use, along with any variables specific to the host I am using. The container can reference an image, either available locally or to be pulled from a registry, such as Docker Hub, if it does not exist. I prefer to fix the tag of the image because `latest` can be volatile. For database containers it is commonplace to map the target port to a different port from the published (host) port. This is so that multiple instances of the same database can run on the same host. The container usually uses the common port for the database, e.g., `5432` for PostgreSQL.

```yml
services:
  database:
    environment:
      - POSTGRES_USER=lesarcs
      - POSTGRES_PASSWORD=lesarcs
      - POSTGRES_DB=lesarcs
    image: postgres:11.1-alpine
    ports:
      -
        published: ${POSTGRES_HOST_PORT}
        target: 5432
```

The host can then take the port from `.env`, which contains:

```sh
ENV_FILE=dev.env
POSTGRES_HOST_PORT=15432
```

We can test the database service by launching only that service, and running some command from `psql` to test that it is running.

```sh
docker-compose up -d database
docker exec -it lesarcs_database_1 psql -U lesarcs -c 'SELECT VERSION();'
```

Or if `psql` is installed locally:

```sh
psql -h <docker_ip> -p 15432 -U lesarcs -c 'SELECT VERSION();'
```

Now we can build the compose file for the `app` that will use the `database`.

```yml
services:
  app:
    ...
```

For the `build` of the `app` service, I want to give specifics of the build. In the `Dockerfile`:

```docker
FROM python:${app_tag}
```

The `app_tag` variable is then defined in the compose YAML, itself located in the current working directory, as specified by `context`.

```yml
app:
  build:
    args:
      from_tag: 3.7.2-alpine3.8
    context: .
  ...
```

The `app` should only launched when its dependencies are also launched.

```yml
app:
  ...
  depends_on:
    - database
  ...
```

The `app` can get environment variables from an `env_file` specific to the context, and `environment` for things that are specific to the project. The `env_file` in this context is referenced in `.env` and contains a single line `SCHEMANAME=gollet`.

```yml
app:
  ...
  env_file:
    - ${ENV_FILE}
  environment:
    TABLENAME: lutins
  ...
```

To modify `app` service code on the host machine the we can `bind`, mapping the `source` directory on the host to the `target` on the container. Changes in this volume by both host and container will be reflected in the other. In practice, this is only for development. In production, we should use `ADD` or `COPY` instructions in the `Dockerfile`.

```yml
app:
  ...
  volumes:
    -
      type: bind
      source: ./app
      target: /app
  ...
```

The `command` key in the `app` service is for defining what the container should do upon launch. This overrides any `CMD` instruction in the `Dockerfile`.

```yml
app:
  ...
  command:
    - ls
    - -al
  ...
```

The `app` container will exit immediately. To keep it alive, change the command to something that does not terminate immediately, and add a pseudo-terminal, like the '-t' flag for `docker run`.

```yml
app:
  ...
  command:
    - sh
  tty: true
  ...
```

Then to get the the terminal, from where we can run anything available to the container itself, such as the Python app.

```sh
docker-compose up -d
docker exec -it lesarcs_app_1 python
```

## Other things I have found useful

### Checking the evaluation of environment variables

The `config` command will evaluate the variables used in the YAML file so that you can see before build/run what result of the variable substitution will be.

```sh
docker-compose config
```

### Launching a second set of services

If you are launching a second set of services from the same directory as another set of services, use the `-p` project flag to specify an alternative name, to avoid a namespace collision.

```sh
docker-compose -p another_instance up -d
```

### .env, ARG, ENV, env_file

There is a nice writeup on how to use environment variables [here](https://vsupalov.com/docker-arg-env-variable-guide/). In summary:

* The `.env` file is used by docker-compose.yml in place of `$VAR`
* `ARG` variables are only available during build
* `ENV` variables are available to the container
* An `env_file` is a way to provide a list of environment variables from outside the YAML configuration.

## Summary

I have demonstrated the use of `docker-compose` with a YAML file to replace the use of long and complicated `docker build` and `docker run` commands. I introduced four ways to manipulate environment variables for use at build time and run time. These examples are the foundation for more complex orchestration of multi-container services.
