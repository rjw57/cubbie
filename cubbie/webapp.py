"""
WSGI-compatible web application object for cubbie.

"""
from flask import Flask
from cubbie.model import db

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app
