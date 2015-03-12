"""
Generate fake data for the database.

These functions all require that app.debug==True.

"""
from functools import wraps
from datetime import datetime, timedelta

from faker import Faker
from flask import current_app
from mixer.backend.flask import mixer

from cubbie.model import User, Production, Performance, SalesDatum, Capability

class FixtureError(RuntimeError):
    pass

# A little decorator which ensures that app.debug is True
def debug_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_app.debug:
            raise FixtureError("app.debug must be True")
        return f(*args, **kwargs)
    return wrapper

# Global Faker instance used to create fixtures.
fake = Faker()

@debug_only
def create_user_fixtures(n=5):
    """Create test fixtures for User. Requires app.debug==True."""
    mixer.cycle(n).blend(User, displayname=fake.name, is_active=mixer.RANDOM)

@debug_only
def create_production_fixtures(n=5):
    """Create test fixtures for Production. Requires app.debug==True."""
    mixer.cycle(n).blend(Production, name=fake.sentence, slug=fake.slug)

@debug_only
def create_performance_fixtures(n=20):
    """Create test fixtures for Performance. Requires app.debug==True and >0
    Productions in database.

    """
    def sa(c):
        return datetime.utcnow() + timedelta(minutes=10+5*c)

    def ea(c):
        return datetime.utcnow() + timedelta(minutes=20+15*c)

    mixer.cycle(n).blend(Performance,
        starts_at=mixer.sequence(sa),
        ends_at=mixer.sequence(ea),
        production=mixer.SELECT,
        is_cancelled=mixer.RANDOM,
        is_deleted=mixer.RANDOM,
    )

@debug_only
def create_sales_fixtures(n=20):
    """Create test fixtures for SalesDatum. Requires app.debug==True and >0
    Performances in database.

    """
    from random import seed, randint

    def ma(c):
        return datetime.utcnow() + timedelta(days=randint(1,100))
    def sold(c):
        seed(c)
        return randint(0, 65)
    def avail(c):
        seed(c)
        s = randint(0, 65)
        return s + randint(0, 30)

    mixer.cycle(n).blend(SalesDatum,
        measured_at=mixer.sequence(ma),
        performance=mixer.SELECT,
        is_valid=mixer.RANDOM,
        sold=mixer.sequence(sold),
        available=mixer.sequence(avail),
    )

@debug_only
def create_capability_fixtures(n=20):
    """Create test fixtures for Capability. Requires app.debug==True and >0
    Users and >0 Productions in database.

    """

    mixer.cycle(n).blend(Capability,
        user=mixer.SELECT,
        production=mixer.SELECT,
    )
