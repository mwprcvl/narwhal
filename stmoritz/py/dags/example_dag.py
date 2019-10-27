""" example dag

to get airflow going, run the following commands:

export AIRFLOW_HOME=/app
airflow initdb
airflow webserver
airflow scheduler

to run the dag:

airflow test my_hello_dag print_hello 2019-10-22
airflow trigger_dag my_hello_dag

"""

import datetime as dt

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def print_something(arg):
    """ simple output """
    print(f'{arg}')


DEFAULT_ARGS = {
    'owner': 'airflow',
    'start_date': dt.datetime(2017, 6, 1),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}


with DAG('my_hello_dag', default_args=DEFAULT_ARGS) as my_dag:

    PRINT_HELLO = PythonOperator(
        task_id='print_hello', python_callable=print_something,
        op_kwargs={'arg': 'Starting'})

    PRINT_GOODBYE = PythonOperator(
        task_id='print_goodbye', python_callable=print_something,
        op_kwargs={'arg': 'Ending'})

PRINT_HELLO >> PRINT_GOODBYE
