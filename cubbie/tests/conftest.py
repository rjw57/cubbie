"""
Various useful pytest fixtures and configuration.

"""

from flask.ext.migrate import Migrate, upgrade, downgrade
import pytest

from cubbie.webapp import create_app, db as _db

@pytest.fixture(scope='session')
def app(request):
    app = create_app()
    app.config.from_object(dict(
        # Create an in-memory database
        SQLALCHEMY_DATABASE_URI='sqlite://',

        # Enable testing
        TESTING=True,
    ))

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app

@pytest.fixture(scope='session')
def db(app, request):
    _db.app = app

    def teardown():
        _db.drop_all()

    request.addfinalizer(teardown)
    return _db

@pytest.fixture(scope='session')
def migrate(app, db):
    return Migrate(app, db)

@pytest.fixture(scope='function')
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

