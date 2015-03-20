"""
Test Production model

"""
import pytest
from mixer.backend.flask import mixer

from cubbie.model import Production, Capability
from cubbie.fixture import create_production_fixtures

def test_fixtures_created(productions):
    """The production fixture should have > 3 productions."""
    assert Production.query.count() > 3

def test_delete_production_cascades_capabilities(session, productions, users):
    cap = mixer.blend(Capability, user=mixer.SELECT, production=mixer.SELECT)
    cap_prod = cap.production
    session.add(cap)
    session.commit()

    cap_id = cap.id
    assert Capability.query.get(cap_id) is not None

    session.delete(cap_prod)
    session.commit()
    assert Capability.query.get(cap_id) is None
