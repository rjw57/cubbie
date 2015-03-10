"""
Test Production model

"""
import pytest

from cubbie.model import Production
from cubbie.fixture import create_production_fixtures

def test_fixtures_created(productions):
    """The production fixture should have > 3 productions."""
    assert Production.query.count() > 3

