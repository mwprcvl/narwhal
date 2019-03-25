#!/usr/bin/env make
#
# makefile for project commands
#

proj := "stmoritz"
db_host_port := "15432"
local := "192.168.99.100"
remote := "remote_host_tbd"
sshkey := "~/.ssh/id_rsa"

build:
	@docker-compose build

up:
	@docker-compose up -d

down:
	@docker-compose down

psql:
	@psql -h ${local} -p ${db_host_port} -U ${proj} -d ${proj}

bashdb:
	@docker exec -it ${proj}_db_1 bash

bashpy:
	@docker exec -it ${proj}_py_1 bash

app:
	@docker exec -it ${proj}_py_1 bash /app/run_app.sh

sync:
	@echo "sync ${PWD} with ${remote}:${proj}"
	@rsync -avqz -e "ssh -i ${sshkey}" --delete --filter ":- .gitignore" --filter "- .git/" . ${remote}:${proj}/
	@echo "sync complete"

getnb:
	@echo "fetching jupyter notebooks from ${remote}"
	@rsync -avqz -e "ssh -i ${sshkey}" ${remote}:${proj}/py/notebooks/ py/notebooks/
	@echo "sync complete"
