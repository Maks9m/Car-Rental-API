import pytest
from decimal import Decimal
from datetime import datetime, timedelta

def calculate_test_price(start, end, hourly_rate):
    duration = end - start
    minutes = max(1, duration.total_seconds() / 60)
    return (Decimal(minutes) * (hourly_rate / Decimal(60))).quantize(Decimal("0.01"))

def test_calculate_trip_price_logic():
    """Тестування чистої бізнес-логіки без БД"""
    start = datetime(2025, 1, 1, 12, 0)
    
    # Кейс 1: 1 година при 600/год = 600
    end_1h = start + timedelta(hours=1)
    assert calculate_test_price(start, end_1h, Decimal("600.00")) == Decimal("600.00")
    
    # Кейс 2: 15 хвилин при 600/год = 150
    end_15m = start + timedelta(minutes=15)
    assert calculate_test_price(start, end_15m, Decimal("600.00")) == Decimal("150.00")