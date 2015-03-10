"""
Test SalesDatum model

"""
import pytest
from sqlalchemy.exc import IntegrityError

from cubbie.model import SalesDatum

def test_inconsistent_sales(mixer, session, performances):
    """Creating an inconsistent sales datum fails."""
    with pytest.raises(IntegrityError):
        s = mixer.blend(SalesDatum,
            sold=5, available=3, performance=mixer.SELECT)

def test_consistent_sales(mixer, session, performances):
    """Creating an sales datum where sold == available succeeds."""
    s = mixer.blend(SalesDatum, sold=5, available=5, performance=mixer.SELECT)

def test_zero_sales(mixer, session, performances):
    """Creating an sales datum where sold == 0 succeeds."""
    s = mixer.blend(SalesDatum, sold=0, available=5, performance=mixer.SELECT)

def test_negative_sales(mixer, session, performances):
    """Creating an sales datum where sold -ve fails."""
    with pytest.raises(IntegrityError):
        s = mixer.blend(SalesDatum, sold=-5, available=5,
                performance=mixer.SELECT)

def test_negative_available(mixer, session, performances):
    """Creating an sales datum where available -ve fails."""
    with pytest.raises(IntegrityError):
        s = mixer.blend(SalesDatum, available=-5, performance=mixer.SELECT)


