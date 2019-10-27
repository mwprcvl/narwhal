#!/usr/bin/env python3

""" simplest flask example

run from CLI with:

python flask_app.py

"""


from flask import Flask


APP = Flask(__name__)


@APP.route('/')
def hello_world():
    """ say hello """
    return "Hello, world!"


if __name__ == "__main__":
    APP.run(debug=True, host='0.0.0.0')
