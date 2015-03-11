"""
Various useful pytest fixtures and configuration.

"""
import uuid

from faker import Factory
from flask.ext.migrate import Migrate, upgrade, downgrade
from mixer.backend.flask import mixer
import pytest
from testing.postgresql import Postgresql

from cubbie.webapp import create_app
from cubbie.auth import make_user_token
from cubbie.model import db
from cubbie.model import User, Capability
from cubbie.fixture import (
    create_user_fixtures, create_performance_fixtures, create_production_fixtures,
    create_capability_fixtures
)

@pytest.fixture(scope='module')
def temp_psql(request):
    # Create temporary database
    psql = Postgresql()

    def teardown():
        psql.stop()
    request.addfinalizer(teardown)

    return psql

@pytest.fixture(scope='module')
def app(request, temp_psql):
    app = create_app()

    class TestConfig():
        # Create an temporary database
        SQLALCHEMY_DATABASE_URI=temp_psql.url()

        # Enable testing
        TESTING=True

        # Enable debug
        DEBUG=True

        # Super-secret JWT key
        JWT_SECRET_KEY=uuid.uuid4().hex

    app.config.from_object(TestConfig)

    # Initialise various DB dependent bits of app
    mixer.init_app(app)
    db.init_app(app)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    # Upgrade the (blank) database to the latest schema
    Migrate(app, db)
    upgrade()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app

@pytest.fixture()
def session(app, request):
    """Creates a new database session for a test."""
    # Remove any data already in the database.
    db.drop_all()
    db.create_all()

    def teardown():
        db.session.rollback()

    request.addfinalizer(teardown)
    return db.session

@pytest.fixture()
def users(session):
    """Create mock users."""
    create_user_fixtures(5)

@pytest.fixture()
def productions(session):
    create_production_fixtures(5)

@pytest.fixture()
def performances(session, productions):
    create_performance_fixtures(15)
    create_production_fixtures(5)

@pytest.fixture()
def capabilities(session, productions, users):
    create_capability_fixtures(15)

@pytest.fixture()
def member_user(session, capabilities):
    """A user who is a member of a production."""
    u = mixer.blend(User, displayname='testuser')
    mixer.blend(Capability, user=u, type='member', production=mixer.SELECT)
    return u

@pytest.fixture()
def member_token(member_user):
    """A token for member_user"""
    return make_user_token(member_user)

@pytest.fixture()
def fake():
    """A faker instance."""
    return Factory().create()
