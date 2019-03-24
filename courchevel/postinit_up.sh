#!/usr/bin/env bash
#
# copy the post-initialization data volume and launch a container from it
rm -r ./db_data_postinit
mkdir -p ./db_data_postinit
cp -r ./db_data/* ./db_data_postinit
docker-compose -f docker-compose-postinit.yml -p courchevelpostinit up -d
