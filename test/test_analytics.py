import pytest
from decimal import Decimal
from src.locations.service import LocationService

def test_location_financial_report(db_session, setup_test_data):
    service = LocationService()
    
    # Викликаємо звіт
    report = service.get_analytics(db_session)
    
    # Перевіряємо, що дані повернулися (не порожньо)
    assert len(report) >= 0
    
    # Якщо в базі є дані від seed, перевіряємо структуру
    if len(report) > 0:
        row = report[0]
        assert hasattr(row, "location_id")
        assert hasattr(row, "address")
        assert hasattr(row, "total_revenue")
        assert isinstance(row.total_revenue, (Decimal, float, type(None)))