import pytest
from unittest.mock import patch
from src.trips.service import TripService
from src.exceptions import BadRequest
from src.models import Trip

def test_finish_trip_atomic_rollback(db_session, setup_test_data):
    """Перевірка атомарності: якщо платіж не створився, поїздка не завершується"""
    service = TripService()
    
    # 1. Знаходимо активну поїздку
    from src.models import Trip
    trip = db_session.query(Trip).filter(Trip.end_time == None).first()
    if not trip:
        pytest.skip("No active trips to test rollback")

    # 2. Імітуємо помилку в репозиторії платежів
    with patch("src.payments.repository.PaymentRepository.create_pending_payment") as mocked_payment:
        mocked_payment.side_effect = Exception("Database Crash!")

        # 3. Намагаємося завершити поїздку
        with pytest.raises(BadRequest):
            service.finish_trip(db_session, trip.trip_id, end_location_id=1)
        
        # 4. ПЕРЕВІРКА ROLLBACK
        db_session.expire_all() # Очищуємо кеш сесії
        updated_trip = db_session.get(Trip, trip.trip_id)
        
        # Поїздка НЕ повинна бути завершена, бо транзакція відкотилася
        assert updated_trip.end_time is None
        assert updated_trip.price is None