# makefile for docker commands
#
# arguments:
#  echo :: return version name
#  build :: build using docker
#  run :: run the container
#. cmd :: run a command through entrypoint
#  tag :: tag the image
# options:
#  ver :: semantic version specified by user
#
# usage:
# make ver="1.1" echo
# make build
# make run
# make cmd
# make ver="1.1" tag

IMAGE_NAME := 'valthorens'
LATEST := ${IMAGE_NAME}:latest
VER := ${IMAGE_NAME}:$(ver)

echo:
	@echo ${VER}

build:
	@docker build --rm -t ${IMAGE_NAME} .

run:
	@docker run --rm -it ${IMAGE_NAME} bash -c 'env|grep ev_*'

cmd:
	@docker run --rm -it ${IMAGE_NAME} default

tag:
	@docker tag ${LATEST} ${VER}
