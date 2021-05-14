# app/__init__.py

from flask import Flask, request
import logging

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Load the config file
app.config.from_object('config')

app.secret_key = 'super secret key'
