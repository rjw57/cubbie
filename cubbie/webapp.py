"""
WSGI-compatible web application object for cubbie.

"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# This needs to be created outside of create_...() in order that Models can be
# defined
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app
