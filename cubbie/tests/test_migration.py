"""Test database migration via Flask-Migrate.

"""
from flask.ext.migrate import upgrade, downgrade

from cubbie.model import db

def test_upgrade(app):
    """Database upgrade from a blank database should succeed."""
    with db.engine.begin():
        db.drop_all()
        upgrade()

def test_null_upgrade(app):
    """Database upgrade after create_all() should succeed."""
    with db.engine.begin():
        db.create_all()
        upgrade()

def test_downgrade(app):
    """Database downgrade to 'base' after upgrade should succeed."""
    with db.engine.begin():
        upgrade()
        downgrade(revision='base')

