"""
Test SalesDatum model

"""
from mixer.backend.flask import mixer
import pytest
from sqlalchemy.exc import IntegrityError

from cubbie.model import SalesDatum

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


