# A simple python service with jupyter lab, rstudio, and a database container

## Purpose

Document the steps involved in setting up containers containing a Python development environment and a PostgreSQL database.

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
PROJECT=stmoritz
POSTGRES_DB_HOST=db
POSTGRES_DB_PORT=5432
DB_INIT_SCRIPTS_PATH=db_init
ENV_FILE=dev.env
POSTGRES_DB_HOST_PORT=15432
PY_DEBUG_PORT=13000
PY_ENVIRONMENT_FILE=environment.yml
PY_NOTEBOOK_PORT=18888
```

## PostgreSQL database service

For PostgreSQL, I configure the image with a custom username, custom port, and a Docker volume for persisting data as described (here)[3_courchevel.md]. The service has a volume like:

```yml
services:
  db:
    volumes:
      -
        type: volume
        source: db_1
        target: /var/lib/postgresql/data
```

The Docker volume itself is declared as a top level item:

```yml
volumes:
  db_1:
```

Docker recommend using volumes like this for persisting data.

The `db_init` directory is for any scripts that should run upon launching the container for the first time.

## Python and JupyterLab service

For Python, I configure the image as described (here)[4_saasfee.md]. Local directories for Python application code and JupyterLab on the container are also local volumes.

```yml
services:
  py:
    volumes:
      -
        type: bind
        source: ./py/lab
        target: /lab
      -
        type: bind
        source: ./py/app
        target: /app
```

### Debugging Python container from localhost

With the configuration of binding volumes to make editing code locally possible, VSCode also can be configured to debug the container using the container's Python interpreter. I configure debug ports in the Compose YAML:

```
services:
  py:
    ports:
      -
        published: ${PY_DEBUG_PORT}
        target: 3000
```

Within VSCode, we set the debug port and the path mappings. *This must be in the project directory*. I am running a VM with Docker, so instead of localhost, `127.0.0.1`, I have the VM's IP address, `192.168.99.100`.

```
{
   "version": "0.2.0",
    "configurations": [
        {
            "name": "Attach (Remote Debug)",
            "type": "python",
            "request": "attach",
            "port": 13000,
            "host": "192.168.99.100",
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

The application to be debugged will need some additional code upfront. Here I assume port 3000 and localhost for the container.

```python
import ptvsd
print("Waiting to attach")
address = ('0.0.0.0', 3000)
ptvsd.enable_attach(address)
ptvsd.wait_for_attach(timeout=10)
```

With these items in place, set a breakpoint, start the application on the container, then start the debug session in VSCode. With the containers running, I have a command in the `Makefile` to run the app.

```sh
docker exec -it stmoritz_py_1 bash /app/run_app.sh
```

A debug console should now be available at the breakpoint that was set.

### Sharing and syncing with remote host

Debugging a remote host can be challenging in some highly restricted environments, for example a debug port might not be available. A simple alternative is to use `rsync` to push code changes to the remote without involving `git`. I roll in an ssh key to avoid having to enter my password on each sync, and put everything as a command in the `Makefile`.

```
sync:
  @echo "sync ${PWD} with ${remote}:${proj}"
  @rsync -avqz -e "ssh -i ${sshkey}" --delete --filter ":- .gitignore" --filter "- .git/" . ${remote}:${proj}/
  @echo "sync complete"
```

## R and Rstudio service

For Rstudio, I configure the image as described (here)[4_whistler.md]. Local directories for R code on the container are also local volumes.

```yml
services:
  rs:
    volumes:
    -
      type: bind
      source: ./rs/r
      target: /home/rstudio
```

I put a file `/home/rstudio/.Renviron` in the Rstudio container with appropriate environment variables for connecting to the database container.

```sh
DB_HOST=db
DB_PORT=5432
DB_NAME=stmoritz
DB_USER=stmoritz
DB_PASS=stmoritz
```

To demonstrate that I can connect to the database, I use an Rscript created locally (`./rs/r/db_conn.R`) that gets put into the container's home directory.

```r
readRenviron(".Renviron")

library(RPostgreSQL)

conn <- dbConnect(
  RPostgreSQL::PostgreSQL(),
  host = Sys.getenv("DB_HOST"),
  port = Sys.getenv("DB_PORT"),
  dbname = Sys.getenv("DB_NAME"),
  user = Sys.getenv("DB_USER"),
  password = Sys.getenv("DB_PASS"))

res <- dbGetQuery(conn, "SELECT VERSION();")

print(res)

dbDisconnect(conn)
```

I get the reassuring output that I connected to the expected database version.

```
PostgreSQL 11.2 on x86_64-pc-linux-musl, compiled by gcc (Alpine 8.2.0) 8.2.0, 64-bit
```

## Summary

I have demonstrated how to configure a PostgreSQL database container with Anaconda Python and Jupyter. I have shown how to use VSCode to debug code on the container from a local VSCode IDE.