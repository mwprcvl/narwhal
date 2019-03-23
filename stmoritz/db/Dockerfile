# use a base image with small OS
ARG base_tag="11.2-alpine"
FROM postgres:${base_tag}

ARG init_scripts_path="db_init"
COPY ${init_scripts_path} /docker-entrypoint-initdb.d/
