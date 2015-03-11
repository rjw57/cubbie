"""
Test Performance model

"""
from mixer.backend.flask import mixer
import pytest
from sqlalchemy.exc import IntegrityError

from cubbie.model import Performance
from cubbie.fixture import (
    create_performance_fixtures, create_production_fixtures
)

def test_fixtures_created(performances):
    assert Performance.query.count() > 0

def test_negative_duration(performances):
    """Creating a negative duration performance fails."""
    from datetime import timedelta, datetime
    now = datetime.utcnow()
    with pytest.raises(IntegrityError):
        s = mixer.blend(Performance,
                starts_at=now, ends_at=now - timedelta(minutes=1))

def test_creation(productions):
    """Creating a performance succeeds."""
    from datetime import timedelta, datetime
    now = datetime.utcnow()
    s = mixer.blend(
        Performance, starts_at=now, ends_at=now + timedelta(minutes=1),
        production=mixer.SELECT
    )

