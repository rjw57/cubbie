"""
General API tests.

"""
import json

from flask import url_for

from cubbie.auth import make_user_token
from cubbie.model import db

def auth_headers(token):
    """Return a list of Authorization headers corresponding to token."""
    return [('Authorization', 'Bearer %s' % token)]

def test_verify_no_token(client):
    """Verification endpoint requires authentication."""
    resp = client.get(url_for('api.verify_token'))
    assert resp.status_code == 401

def test_verify_no_user(client, member_user):
    """Passing a valid token for an invalid user fails."""
    # Get a token for a user
    token = make_user_token(member_user)

    # Now, delete the user
    member_user.is_active = False
    db.session.add(member_user)
    db.session.commit()

    # Verify the token
    resp = client.get(
        url_for('api.verify_token'), headers=auth_headers(token)
    )
    assert resp.status_code == 401 # Unauthorized

def test_verify_user(client, member_user):
    """Passing a valid token for an valid user succeeds."""
    # Get a token for a user
    token = make_user_token(member_user)

    # User's active, yes?
    assert member_user.is_active

    # Verify the token
    resp = client.get(
        url_for('api.verify_token'), headers=auth_headers(token)
    )
    assert resp.status_code == 200

    # should succeed
    assert resp.json['status'] == 'ok'

