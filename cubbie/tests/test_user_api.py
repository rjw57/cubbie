"""
Test user profile API.

"""
from flask import url_for
from mixer.backend.flask import mixer

from cubbie.model import Capability, Production, User

def auth_headers(token):
    """Return a list of Authorization headers corresponding to token."""
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

def test_profile_productions(client, member_token, member_user):
    """The user is a member of all the productions in the profile."""
    # Add user as a member to some more productions
    mixer.cycle(3).blend(Capability, user=member_user, production=mixer.SELECT, type='member')

    # Getting profile succeeds
    resp = client.get(url_for('api.profile'), headers=auth_headers(member_token))
    assert resp.status_code == 200

    # The number of productions match
    resp_prods = resp.json['productions']
    assert len(resp_prods) == len(member_user.productions)

    # The user is indeed a member (of some sort) of each production
    for p_record in resp_prods:
        p = Production.query.get(p_record['id'])
        assert member_user in p.users
        assert p in member_user.productions
