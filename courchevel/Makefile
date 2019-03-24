# makefile for docker commands
#
# arguments:
#  build :: build using docker-compose
#  up :: run the containers
#  down :: stop the containers
#  tag :: tag the image as postinit
#  rm :: remove a container
#  reset :: remove the database volume data
#  config :: see how docker compose will be configures from environment
#  commit :: commit a snapshot of the container
#  postrestart :: restart the database post initialization
#  postup :: start the database post initialization
#  postdown :: stop the database post initialization

proj := courchevel
LATEST := ${proj}:latest
VER := ${proj}:postinit
CONTAINER_NAME := ${proj}_db_1

build:
	@docker-compose build

up:
	@docker-compose up -d

down:
	@docker-compose down

psql:
	@psql -h 192.168.99.100 -p 15432 -U ${proj} -d ${proj}

rmclonedvol:
	@docker volume rm ${proj}postinit_db_1

clonevol:
	@bash docker_volume_clone.sh ${proj}_db_1 ${proj}postinit_db_1

tag:
	@docker tag ${LATEST} ${VER}

rm:
	@docker rm ${CONTAINER_NAME}

reset:
	@rm -rf ./db_data/*

config:
	@docker-compose config

commit:
	@docker commit ${CONTAINER_NAME} ${proj}:postinit

postrestart:
	@bash postinit_up.sh

postup:
	@docker-compose -f docker-compose-postinit.yml -p ${proj}postinit up -d

postdown:
	@docker-compose -f docker-compose-postinit.yml -p ${proj}postinit down

psqlpostinit:
	@psql -h 192.168.99.100 -p 15433 -U ${proj} -d ${proj}
