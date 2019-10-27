#!/usr/bin/env python3

"""
demonstrate call to application
"""

import os

# debug setup
# import ptvsd
# print("Waiting to attach")
# address = ('0.0.0.0', 3000)
# ptvsd.enable_attach(address)
# ptvsd.wait_for_attach(timeout=10)


# rest of code
import pandas as pd
import sqlalchemy as sa


template = '{dialect}+{driver}://{user}:{pass}@{host}:{port}/{name}'

db_url_params = {
    'dialect': 'postgresql',
    'driver': 'psycopg2',
    'host': os.environ['DB_HOST'],
    'name': os.environ['DB_NAME'],
    'user': os.environ['DB_USER'],
    'port': os.environ['DB_PORT'],
    'pass': os.environ['DB_PASS']}

engine = sa.create_engine(template.format(**db_url_params))

res = engine.execute("SELECT VERSION();").fetchall()
# res="Hello, world!"
print(res)
