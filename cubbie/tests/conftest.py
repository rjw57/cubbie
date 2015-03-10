"""
Various useful pytest fixtures and configuration.

"""
import uuid

from flask.ext.migrate import Migrate, upgrade, downgrade
from mixer.backend.flask import mixer as _mixer
import pytest
from testing.postgresql import Postgresql

from cubbie.webapp import create_app
from cubbie.auth import make_user_token
from cubbie.model import db as _db
from cubbie.model import User, Capability
from cubbie.fixture import (
    create_user_fixtures, create_performance_fixtures, create_production_fixtures,
    create_capability_fixtures
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

    class TestConfig():
        # Create an temporary database
        SQLALCHEMY_DATABASE_URI=postgresql.url()

        # Enable testing
        TESTING=True

        # Enable debug
        DEBUG=True

        # Super-secret JWT key
        JWT_SECRET_KEY=uuid.uuid4().hex

    app.config.from_object(TestConfig)

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
    create_production_fixtures(5)

@pytest.fixture()
def capabilities(mixer, session, productions, users):
    create_capability_fixtures(15)

@pytest.fixture()
def member_user(mixer, session, capabilities):
    """A user who is a member of a production."""
    u = mixer.blend(User, displayname='testuser')
    mixer.blend(Capability, user=u, type='member', production=mixer.SELECT)
    return u

@pytest.fixture()
def member_token(member_user):
    """A token for member_user"""
    return make_user_token(member_user)
