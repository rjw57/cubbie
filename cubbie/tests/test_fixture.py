"""
Tests for fixtures in general (as opposed to tests which just use them).

"""
from flask import current_app
import pytest
from sqlalchemy.exc import IntegrityError

from cubbie.fixture import (
    FixtureError, create_user_fixtures, create_production_fixtures,
    create_performance_fixtures, create_sales_fixtures, create_capability_fixtures
)
from cubbie.model import User, Production, Performance, SalesDatum, Capability

def test_app_using_postgres(app):
    """The application's SQLALCHEMY_DATABASE_URI config key should point to
    a postgres database."""
    assert app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql://')

def test_current_using_postgres(app):
    """The current application's SQLALCHEMY_DATABASE_URI config key should
    point to a postgres database."""
    assert current_app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql://')

def test_config_using_postgres(config):
    """The SQLALCHEMY_DATABASE_URI key in the config fixture should point to a
    postgres database."""
    assert config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql://')

def test_debug_enabled(app):
    """The defaulkt value of app.debug should be True."""
    assert app.debug

@pytest.mark.app(debug=False)
def test_user_fixtures_require_debug(session, app):
    """Trying to create a user fixture requires app.debug == True."""
    with pytest.raises(FixtureError):
        create_user_fixtures()

@pytest.mark.app(debug=True)
def test_user_fixtures(session):
    """User fixtures are created."""
    assert User.query.count() == 0
    create_user_fixtures()
    assert User.query.count() > 0

@pytest.mark.app(debug=False)
def test_production_fixtures_require_debug(session):
    """Trying to create a production fixture requires app.debug == True."""
    with pytest.raises(FixtureError):
        create_production_fixtures()

@pytest.mark.app(debug=True)
def test_production_fixtures(session):
    """Production fixtures are created."""
    assert Production.query.count() == 0
    create_production_fixtures()
    assert Production.query.count() > 0

@pytest.mark.app(debug=False)
def test_performance_fixtures_require_debug(session, app):
    """Trying to create a performance fixture requires app.debug == True."""
    app.debug = True
    create_production_fixtures() # required for performances
    app.debug = False

    with pytest.raises(FixtureError):
        create_performance_fixtures()

@pytest.mark.app(debug=True)
def test_performance_fixtures_need_productions(session):
    """Performance fixtures are created only when there are productions."""
    with pytest.raises(IntegrityError):
        create_performance_fixtures()

@pytest.mark.app(debug=True)
def test_performance_fixtures(session):
    """Performance fixtures are created."""
    create_production_fixtures() # required for performances
    assert Performance.query.count() == 0
    create_performance_fixtures()
    assert Performance.query.count() > 0

@pytest.mark.app(debug=False)
def test_sales_fixtures_require_debug(session, app):
    """Trying to create a sales fixture requires app.debug == True."""
    app.debug = True
    create_production_fixtures()
    create_performance_fixtures()
    app.debug = False

    with pytest.raises(FixtureError):
        create_sales_fixtures()

@pytest.mark.app(debug=True)
def test_sales_fixtures_need_performances(session):
    """SalesDatum fixtures are created only when there are >0 performances."""
    create_production_fixtures() # but no performances
    with pytest.raises(IntegrityError):
        create_sales_fixtures()

@pytest.mark.app(debug=True)
def test_capability_fixtures(session):
    """Capability fixtures are created."""
    create_production_fixtures() # required for performances
    create_performance_fixtures() # required for capabilities
    assert Capability.query.count() == 0
    create_capability_fixtures()
    assert Capability.query.count() > 0

@pytest.mark.app(debug=False)
def test_capability_fixtures_require_debug(session, app):
    """Trying to create a capabilities fixture requires app.debug == True."""
    app.debug = True
    create_production_fixtures()
    create_performance_fixtures()
    create_user_fixtures()
    app.debug = False

    with pytest.raises(FixtureError):
        create_capability_fixtures()

@pytest.mark.app(debug=True)
def test_capability_fixtures_need_users(session):
    """Capability fixtures are created only when there are >0 users."""
    create_production_fixtures()
    with pytest.raises(IntegrityError):
        create_capability_fixtures()

@pytest.mark.app(debug=True)
def test_capability_fixtures_need_performances(session):
    """Capability fixtures are created only when there are >0 productions."""
    create_user_fixtures()
    with pytest.raises(IntegrityError):
        create_capability_fixtures()

@pytest.mark.app(debug=True)
def test_capability_fixtures(session):
    """Capability fixtures are created."""
    create_production_fixtures() # required for capabilities
    create_user_fixtures() # required for capabilities
    assert Capability.query.count() == 0
    create_capability_fixtures()
    assert Capability.query.count() > 0

def test_member_user_fixture(member_user):
    """The "member" user is indeed a member of some production and only a member."""
    prods = User.query.filter(User.id == member_user.id).join(Capability).join(Production)
    prods = prods.filter(Capability.type == 'member')
    prods = prods.with_entities(User.displayname, Capability.type, Production.id).all()

    assert len(prods) == 1
    for n, t, p_id in prods:
        assert n == member_user.displayname
        assert t == 'member'
        assert p_id is not None

    # Check that the user is not some other class of user
    prods = User.query.filter(User.id == member_user.id).join(Capability).join(Production)
    prods = prods.with_entities(User.displayname, Capability.type, Production.id).all()
    assert len(prods) == 1
