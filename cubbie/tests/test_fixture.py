"""
Tests for fixtures in general (as opposed to tests which just use them).

"""
import pytest
from sqlalchemy.exc import IntegrityError

from cubbie.fixture import (
    FixtureError, create_user_fixtures, create_production_fixtures,
    create_performance_fixtures, create_sales_fixtures, create_capability_fixtures
)
from cubbie.model import User, Production, Performance, SalesDatum, Capability

@pytest.mark.app(debug=False)
def test_user_fixtures_require_debug(app, mixer):
    """Trying to create a user fixture requires app.debug == True."""
    assert app.debug == False
    with pytest.raises(FixtureError):
        create_user_fixtures()

@pytest.mark.app(debug=True)
def test_user_fixtures(mixer):
    """User fixtures are created."""
    assert User.query.count() == 0
    create_user_fixtures()
    assert User.query.count() > 0

@pytest.mark.app(debug=False)
def test_production_fixtures_require_debug(app, mixer):
    """Trying to create a production fixture requires app.debug == True."""
    assert app.debug == False
    with pytest.raises(FixtureError):
        create_production_fixtures()

@pytest.mark.app(debug=True)
def test_production_fixtures(mixer):
    """Production fixtures are created."""
    assert Production.query.count() == 0
    create_production_fixtures()
    assert Production.query.count() > 0

@pytest.mark.app(debug=False)
def test_performance_fixtures_require_debug(app, mixer):
    """Trying to create a performance fixture requires app.debug == True."""
    app.debug = True
    create_production_fixtures() # required for performances
    app.debug = False

    assert app.debug == False
    with pytest.raises(FixtureError):
        create_performance_fixtures()

@pytest.mark.app(debug=True)
def test_performance_fixtures_need_productions(mixer):
    """Performance fixtures are created only when there are productions."""
    with pytest.raises(IntegrityError):
        create_performance_fixtures()

@pytest.mark.app(debug=True)
def test_performance_fixtures(mixer):
    """Performance fixtures are created."""
    create_production_fixtures() # required for performances
    assert Performance.query.count() == 0
    create_performance_fixtures()
    assert Performance.query.count() > 0

@pytest.mark.app(debug=False)
def test_sales_fixtures_require_debug(app, mixer):
    """Trying to create a sales fixture requires app.debug == True."""
    app.debug = True
    create_production_fixtures()
    create_performance_fixtures()
    app.debug = False

    assert app.debug == False
    with pytest.raises(FixtureError):
        create_sales_fixtures()

@pytest.mark.app(debug=True)
def test_sales_fixtures_need_performances(mixer):
    """SalesDatum fixtures are created only when there are >0 performances."""
    create_production_fixtures() # but no performances
    with pytest.raises(IntegrityError):
        create_sales_fixtures()

@pytest.mark.app(debug=True)
def test_capability_fixtures(mixer):
    """Capability fixtures are created."""
    create_production_fixtures() # required for performances
    create_performance_fixtures() # required for capabilities
    assert Capability.query.count() == 0
    create_capability_fixtures()
    assert Capability.query.count() > 0

@pytest.mark.app(debug=False)
def test_capability_fixtures_require_debug(app, mixer):
    """Trying to create a capabilities fixture requires app.debug == True."""
    app.debug = True
    create_production_fixtures()
    create_performance_fixtures()
    create_user_fixtures()
    app.debug = False

    assert app.debug == False
    with pytest.raises(FixtureError):
        create_capability_fixtures()

@pytest.mark.app(debug=True)
def test_capability_fixtures_need_users(mixer):
    """Capability fixtures are created only when there are >0 users."""
    create_production_fixtures()
    with pytest.raises(IntegrityError):
        create_capability_fixtures()

@pytest.mark.app(debug=True)
def test_capability_fixtures_need_performances(mixer):
    """Capability fixtures are created only when there are >0 productions."""
    create_user_fixtures()
    with pytest.raises(IntegrityError):
        create_capability_fixtures()

@pytest.mark.app(debug=True)
def test_capability_fixtures(mixer):
    """Capability fixtures are created."""
    create_production_fixtures() # required for capabilities
    create_user_fixtures() # required for capabilities
    assert Capability.query.count() == 0
    create_capability_fixtures()
    assert Capability.query.count() > 0
