"""
Test user profile API.

"""

from flask import url_for

def auth_headers(token):
    """Return a list of Authorization headers correponding to token."""
    return [('Authorization', 'Bearer %s' % token)]

def test_profile_needs_auth(client):
    """Getting the current user's profile without a token is Unauthorized."""
    resp = client.get(url_for('api.profile'))
    assert resp.status_code == 401

def test_profile(client, member_token, member_user):
    """Getting a profile with a valid token succeeds."""
    resp = client.get(url_for('api.profile'), headers=auth_headers(member_token))
    assert resp.status_code == 200
    assert resp.json['_type'] == 'User#profile'
    assert resp.json['displayname'] == member_user.displayname
