"""
Various useful pytest fixtures and configuration.

"""

from flask.ext.migrate import Migrate, upgrade, downgrade
from mixer.backend.flask import mixer as _mixer
import pytest
from testing.postgresql import Postgresql

from cubbie.webapp import create_app
from cubbie.model import db as _db
from cubbie.fixture import (
    create_user_fixtures, create_performance_fixtures, create_production_fixtures
)

@pytest.fixture(scope='session')
def postgresql(request):
    # Create temporary database
    psql = Postgresql()

    def teardown():
        psql.stop()
    request.addfinalizer(teardown)

    return psql

@pytest.fixture(scope='session')
def app(postgresql, request):

    app = create_app()
    app.config.from_object(dict(
        # Create an temporary database
        SQLALCHEMY_DATABASE_URI=postgresql.url(),

        # Enable testing
        TESTING=True,
    ))
    app.debug = True

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app

@pytest.fixture()
def db(app, request):
    _db.app = app
    _db.create_all()

    def teardown():
        _db.drop_all()

    request.addfinalizer(teardown)
    return _db

@pytest.fixture()
def migrate(app, db):
    return Migrate(app, db)

@pytest.fixture()
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection)
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session

@pytest.fixture()
def mixer(app, session):
    _mixer.init_app(app)
    return _mixer

@pytest.fixture()
def users(mixer, session):
    """Create mock users."""
    create_user_fixtures(5)

@pytest.fixture()
def productions(mixer, session):
    create_production_fixtures(5)

@pytest.fixture()
def performances(mixer, session, productions):
    create_performance_fixtures(15)
