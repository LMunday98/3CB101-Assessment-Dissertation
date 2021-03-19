# app/__init__.py

from flask import Flask, request

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the config file
app.config.from_object('web_server.config')

app.secret_key = 'super secret key'