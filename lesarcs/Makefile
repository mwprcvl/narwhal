# makefile for docker commands
#
# arguments:
#  build :: build using docker-compose
#  up :: run the containers
#. down :: stop the containers
#
# usage:
# make build
# make up
# make down

build:
	@docker-compose build

up:
	@docker-compose up -d

down:
	@docker-compose down

py:
	@docker exec -it lesarcs_app_1 python