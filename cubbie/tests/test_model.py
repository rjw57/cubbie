"""Test database models with an in-memory SQLite database.

"""
import pytest

from cubbie.model import User

@pytest.fixture(scope='function')
def users(mixer, session):
    """Create mock users."""
    mixer.cycle(5).blend(User)

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

def test_user_fixtures_created(users, session):
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

