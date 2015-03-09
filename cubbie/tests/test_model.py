"""Test database models with an in-memory SQLite database.

"""
from cubbie.model import User

def test_user_create(session):
    assert User.query.count() == 0
    u = User(displayname='Bob Ferris')
    session.add(u)
    session.commit()
    assert u.id is not None
    assert User.query.count() == 1
    assert User.query.filter_by(displayname='Bob Ferris').count() == 1
    assert User.query.filter_by(displayname='Joe Nonexist').count() == 0

