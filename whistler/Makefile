#!/usr/bin/env make
#
# makefile for docker commands
#

up:
	@docker-compose up -d

down:
	@docker-compose down

bashrs:
	@docker exec -it whistler_rs_1 bash

app:
	@docker exec -it whistler_rs_1 Rscript hello.R
