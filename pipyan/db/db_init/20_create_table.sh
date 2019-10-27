#!/usr/bin/env bash
set -ex

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE SCHEMA ${DUMMY_SCHEMA};
EOSQL
