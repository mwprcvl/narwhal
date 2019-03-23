#!/usr/bin/env make
#
# makefile for docker commands
#

up:
	@docker-compose up -d

down:
	@docker-compose down

psql:
	@psql -h localhost -p 15432 -U stmoritz

bashdb:
	@docker exec -it stmoritz_db_1 bash

bashpy:
	@docker exec -it stmoritz_py_1 bash

app:
	@docker exec -it stmoritz_py_1 bash /app/run_app.sh
