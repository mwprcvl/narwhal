#!/usr/bin/env make
#
# makefile for project commands
#

proj := "pipyan"
db_host_port := "15432"
local := "192.168.99.100"

SHELL := /usr/bin/env bash

build:
	@docker-compose build

up:
	@docker-compose up -d

down:
	@docker-compose down

psql:
	@psql -h ${local} -p ${db_host_port} -U ${proj} -d ${proj}

bashdb:
	@docker exec -it ${proj}_db bash

bashpy:
	@docker exec -it ${proj}_py bash

pyapp:
	@docker exec -it ${proj}_py python /app/app.py

pydb:
	@docker exec -it ${proj}_py python /app/db_app.py

flask:
	@docker exec ${proj}_py nohup bash /app/run_flask.sh > /dev/null 2>&1 &

dash:
	@docker exec ${proj}_py nohup bash /app/run_dash.sh > /dev/null 2>&1 &

air:
	@docker exec ${proj}_py bash /app/run_airflow.sh

check_task:
	@docker exec ${proj}_py airflow test my_hello_dag print_hello 2019-10-22

run_dag:
	@docker exec ${proj}_py airflow trigger_dag my_hello_dag

putdata:
	@docker cp data/. ${proj}_py:/data/

getdata:
	@docker cp ${proj}_py:/data/. data/
