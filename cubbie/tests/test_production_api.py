"""
Test production API

"""
from flask import url_for
from mixer.backend.flask import mixer

from cubbie.fixture import (
    create_performance_fixtures,
    create_sales_fixtures,
    create_capability_fixtures
)
from cubbie.model import db, Capability, Production, User, Performance

def auth_headers(token):
    """Return a list of Authorization headers corresponding to token."""
    return [('Authorization', 'Bearer %s' % token)]

def test_production_404(productions, client):
    resp = client.get(url_for('api.production', slug='does-not-exist'))
    assert resp.status_code == 404

def test_production_get_info(productions, users, client):
    p = Production.query.first()
    create_capability_fixtures(n=3, production=p)
    create_performance_fixtures(n=20, production=p)
    for perf in Performance.query.filter(Performance.production == p):
        create_sales_fixtures(performance=perf)

    resp = client.get(url_for('api.production', slug=p.slug))
    assert resp.status_code == 200
    assert resp.json['_type'] == 'Production#summary'

    j = resp.json

    assert 'name' in j

    assert 'users' in j
    users = j['users']
    assert len(users) > 0
    for u in users:
        assert 'displayname' in u
        assert 'profileUrl' in u
        assert 'type' in u

    assert 'performances' in j
    perfs = j['performances']
    assert len(perfs) > 0
    for perf in perfs:
        assert 'startsAt' in perf
        assert 'duration' in perf
        assert 'performanceUrl' in perf
