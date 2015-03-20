"""
Test SalesDatum model

"""
from mixer.backend.flask import mixer
import pytest
from sqlalchemy.exc import IntegrityError

from cubbie.model import SalesDatum, Performance

def test_inconsistent_sales(performances):
    """Creating an inconsistent sales datum fails."""
    with pytest.raises(IntegrityError):
        s = mixer.blend(SalesDatum,
            sold=5, available=3, performance=mixer.SELECT)

def test_consistent_sales(performances):
    """Creating an sales datum where sold == available succeeds."""
    s = mixer.blend(SalesDatum, sold=5, available=5, performance=mixer.SELECT)

def test_zero_sales(performances):
    """Creating an sales datum where sold == 0 succeeds."""
    s = mixer.blend(SalesDatum, sold=0, available=5, performance=mixer.SELECT)

def test_negative_sales(performances):
    """Creating an sales datum where sold -ve fails."""
    with pytest.raises(IntegrityError):
        s = mixer.blend(SalesDatum, sold=-5, available=5,
                performance=mixer.SELECT)

def test_negative_available(performances):
    """Creating an sales datum where available -ve fails."""
    with pytest.raises(IntegrityError):
        s = mixer.blend(SalesDatum, available=-5, performance=mixer.SELECT)

def test_delete_production(session, performances):
    p = Performance.query.limit(1).first()
    mixer.cycle(10).blend(SalesDatum, available=40, sold=4, performance=p)
    session.commit()

    p_id = p.id
    s_ids = list(
            s.id for s in
            SalesDatum.query.filter(SalesDatum.performance == p)
    )

    assert len(p.sales) > 0
    assert len(s_ids) == len(p.sales)
    session.delete(p)
    session.commit()

    assert SalesDatum.query.filter(
        SalesDatum.performance_id == p_id).count() == 0
    for s_id in s_ids:
        assert SalesDatum.query.get(s_id) is None
