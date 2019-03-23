#!/usr/bin/env bash
#
# copy the post-initialization data volume and launch a container from it
rm -r ./db_data_post_init
mkdir -p ./db_data_post_init
cp -r ./db_data/* ./db_data_post_init
docker-compose -f docker-compose-post_init.yml -p courchevel_post_init up -d
