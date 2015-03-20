"""
Test User model

"""
from mixer.backend.flask import mixer
import pytest
from sqlalchemy.exc import IntegrityError

from cubbie.model import User, UserIdentity, Capability
from cubbie.fixture import create_user_fixtures

def test_create(session):
    """Creating a user should add it to the database."""
    assert User.query.count() == 0
    u = User(displayname='Bob Ferris')
    session.add(u)
    session.commit()
    assert u.id is not None
    assert User.query.count() == 1
    assert User.query.filter_by(displayname='Bob Ferris').count() == 1
    assert User.query.filter_by(displayname='Joe Nonexist').count() == 0

def test_fixtures_created(users):
    """The user fixtures should have more than three users."""
    assert User.query.count() > 0

def test_delete_user(users, session):
    """Deleting a user should also reduce the count by one."""
    u = User.query.first()
    n_u = User.query.count()
    assert u.displayname is not None
    session.delete(u)
    session.commit()
    assert User.query.filter_by(displayname=u.displayname).count() == 0
    assert User.query.count() == n_u - 1

def test_image_url_optional(session, fake):
    """Users need not have an image_url set."""
    u1 = mixer.blend(User, image_url=None)
    session.add(u1) # ok
    u2 = mixer.blend(User, image_url=fake.url)
    session.add(u2) # ok
    session.commit()

def test_default_inactive(session):
    """New users are by default inactive."""
    u = mixer.blend(User, is_active=None)
    session.add(u)
    session.commit()
    assert not User.query.get(u.id).is_active

def test_delete_user_cascades_identity(users, session):
    """Deleting a user with associated identity succeeds."""
    u1 = mixer.blend(User)
    session.add(u1)
    u1id = mixer.blend(UserIdentity, user=u1)
    session.add(u1id)
    session.commit()

    assert User.query.get(u1.id) is not None
    assert UserIdentity.query.get(u1id.id) is not None

    u1_id = u1.id
    u1id_id = u1id.id

    session.delete(u1)
    session.commit()

    assert User.query.get(u1_id) is None
    assert UserIdentity.query.get(u1id_id) is None

def test_delete_user_cascades_capabilities(users, session, productions):
    """Deleting a user with associated capabilitiess succeeds."""
    u1 = mixer.blend(User)
    session.add(u1)
    u1cap = mixer.blend(Capability, user=u1, production=mixer.SELECT)
    session.add(u1cap)
    session.commit()

    assert User.query.get(u1.id) is not None
    assert Capability.query.get(u1cap.id) is not None

    u1_id = u1.id
    u1cap_id = u1cap.id

    session.delete(u1)
    session.commit()

    assert User.query.get(u1_id) is None
    assert Capability.query.get(u1cap_id) is None

def test_delete_user_cascades_production(users, session, productions):
    """Deleting a user with associated productions succeeds."""
    u1 = mixer.blend(User)
    session.add(u1)
    u1cap = mixer.blend(Capability, user=u1, production=mixer.SELECT)
    session.add(u1cap)
    session.commit()

    u1prod = u1.productions[0]
    assert u1 in u1prod.users
    assert User.query.get(u1.id) is not None

    u1_id = u1.id
    session.delete(u1)
    session.commit()

    assert u1 not in u1prod.users
    assert User.query.get(u1_id) is None
