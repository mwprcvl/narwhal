#!/usr/bin/env make
#
# makefile for docker commands
#
proj := saasfee

build:
	@docker-compose build

up:
	@docker-compose -p ${proj} up -d

down:
	@docker-compose -p ${proj} down

bash:
	@docker exec -it ${proj}_py_1 bash

expl:
	@docker exec -it saasfee_py_1 bash -ic "conda list --explicit" > explicit.yml
