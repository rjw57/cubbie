"""Test database migration via Flask-Migrate.

"""

from flask.ext.migrate import upgrade, downgrade

def test_upgrade(db, migrate):
    """Database upgrade from a blank database should succeed."""
    db.drop_all()
    upgrade()

def test_null_upgrade(db, migrate):
    """Database upgrade after create_all() should succeed."""
    db.create_all()
    upgrade()

def test_downgrade(db, migrate):
    """Database downgrade to 'base' after upgrade should succeed."""
    upgrade()
    downgrade(revision='base')

