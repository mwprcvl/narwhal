#!/usr/bin/env bash
airflow initdb
nohup airflow webserver > /dev/null 2>&1 &
nohup airflow scheduler > /dev/null 2>&1 &
