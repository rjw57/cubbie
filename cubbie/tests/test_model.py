"""Test database models with an in-memory SQLite database.

"""
import pytest
from sqlalchemy.exc import IntegrityError

from cubbie.model import User, Production, SalesDatum, Performance

@pytest.fixture()
def users(mixer, session):
    """Create mock users."""
    mixer.cycle(5).blend(User)

@pytest.fixture()
def productions(mixer, session):
    mixer.cycle(5).blend(Production)

@pytest.fixture()
def performances(mixer, session, productions):
    mixer.cycle(5).blend(Performance)

def test_user_create(session):
    """Creating a user should add it to the database."""
    assert User.query.count() == 0
    u = User(displayname='Bob Ferris')
    session.add(u)
    session.commit()
    assert u.id is not None
    assert User.query.count() == 1
    assert User.query.filter_by(displayname='Bob Ferris').count() == 1
    assert User.query.filter_by(displayname='Joe Nonexist').count() == 0

def test_user_fixtures_created(users):
    """The user fixtures should have more than three users."""
    assert User.query.count() > 3

def test_delete_user(users, session):
    """Deleting a user should also reduce the count by one."""
    u = User.query.first()
    n_u = User.query.count()
    assert u.displayname is not None
    session.delete(u)
    session.commit()
    assert User.query.filter_by(displayname=u.displayname).count() == 0
    assert User.query.count() == n_u - 1

def test_productions_creates(productions):
    """The production fixture should have > 3 productions."""
    assert Production.query.count() > 3

def test_inconsistent_sales(mixer, session, productions):
    """Creating an inconsistent sales datum fails."""
    with pytest.raises(IntegrityError):
        s = mixer.blend(SalesDatum, sold=5, available=3)

def test_consistent_sales(mixer, session, productions):
    """Creating an sales datum where sold == available succeeds."""
    s = mixer.blend(SalesDatum, sold=5, available=5)

def test_zero_sales(mixer, session, productions):
    """Creating an sales datum where sold == 0 succeeds."""
    s = mixer.blend(SalesDatum, sold=0, available=5)

def test_consistent_sales(mixer, session, productions):
    """Creating an sales datum where sold -ve fails."""
    with pytest.raises(IntegrityError):
        s = mixer.blend(SalesDatum, sold=-5, available=5)

def test_consistent_sales(mixer, session, productions):
    """Creating an sales datum where available -ve fails."""
    with pytest.raises(IntegrityError):
        s = mixer.blend(SalesDatum, available=-5)

def test_negative_duration_performance(mixer, session, productions):
    """Creating a negative duration performance fails."""
    from datetime import timedelta, datetime
    now = datetime.utcnow()
    with pytest.raises(IntegrityError):
        s = mixer.blend(Performance, starts_at=now, ends_at=now - timedelta(minutes=1))

def test_performance(mixer, session, productions):
    """Creating a performance succeeds."""
    from datetime import timedelta, datetime
    now = datetime.utcnow()
    s = mixer.blend(Performance, starts_at=now, ends_at=now + timedelta(minutes=1))

