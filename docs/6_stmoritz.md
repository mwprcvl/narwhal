# A simple python service with jupyter notebooks and a database container

## Purpose

Document the steps involved in setting up containers containing a Python development environment and a PostgreSQL database.


## Prerequisites

Docker installed. VSCode installed for debugging.


## Project outline

I organize the project to house orchestration files (`Makefile`, `docker-compose.yml`) at the top level, with one subdirectory for each service, each of which contains a `Dockerfile` for the service. The compose file reflects this structure. Relative paths in the compose file are from the directory that the compose file is called from, for example the build context for each image.

```
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

```
PROJECT=stmoritz
POSTGRES_DB_HOST=db
POSTGRES_DB_PORT=5432
POSTGRES_DB_NAME=stmoritz
POSTGRES_DB_USER=stmoritz
POSTGRES_DB_PASS=stmoritz
DB_INIT_SCRIPTS_PATH=db_init
POSTGRES_DB_HOST_PORT=15432
PY_DEBUG_PORT=8001
PY_ENVIRONMENT_FILE=environment.yml
PY_NOTEBOOK_PORT=8000
```

## Database service

For PostgreSQL, I demonstrate how to configure the image with a custom username, custom port, and a Docker volume for persisting data. The service has a volume like:

```
TODO: container volume code
```

The Docker volume itself is declared as a top level item:

```
TODO:
```

Docker recommend using volumes like this for persisting data.

The `db_init` directory is for any scripts that should run upon launching the container for the first time.


## Python service


## Debugging container from local host

With the configuration of binding volumes to make editing code locally possible, VSCode also can be configured to debug the container using the container's Python interpreter. Within VSCode, we set the debug port and the path mappings.

```
{
   "version": "0.2.0",
    "configurations": [
        {
            "name": "Attach (Remote Debug)",
            "type": "python",
            "request": "attach",
            "port": 3000,
            "host": "localhost",
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/py/app",
                    "remoteRoot": "/app"
                }
            ],
            "redirectOutput": false
        }
    ]
}
```

The application to be debugged will need some additional code upfront. Here I assume port 3000 and localhost for the container to debug.

```python
import ptvsd
print("Waiting to attach")
address = ('0.0.0.0', 3000)
ptvsd.enable_attach(address)
ptvsd.wait_for_attach(timeout=10)
```

With these items in place, set a breakpoint, start the application on the container, then start the debug session in VSCode. With the containers running, I have a command in the `Makefile` to run the app.

```sh
app:
  @docker exec -it ${proj}_py_1 bash /app/run_app.sh
```

A debug console should now be available at the breakpoint that was set.


## Sharing and syncing with remote host

Debugging a remote host can be challenging in some highly restricted environments, for example a debug port might not be available. A simple alternative is to use `rsync` to push code changes to the remote without involving `git`. I roll in an ssh key to avoid having to enter my password on each sync, and put everything as a command in the `Makefile`.

```
rsync:
  @echo "sync ${PWD} with ${remote}:${proj}"
  @rsync -avqz -e "ssh -i ${sshkey}" --delete --filter ":- .gitignore" --filter "- .git/" . ${remote}:${proj}/
  @echo "sync complete"
```
