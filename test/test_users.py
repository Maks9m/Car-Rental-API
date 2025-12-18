from fastapi import status
from datetime import date, datetime, timedelta

import pytest

from src.models import Booking, Car, CarLocation, CarModel, CarStatus, DriverLicense, FuelType, LicenseType, Trip, Payment, Status, PaymentType, User

from src.auth.dependencies import get_current_user


def test_get_user_ranking(client, db_session, test_user, test_car):
    """Тест: Рейтинг користувачів (складний SQL запит)"""
    # 1. Створюємо завершене бронювання, поїздку та оплату для test_user
    booking = Booking(
        user_id=test_user.user_id, car_id=test_car.car_id, 
        status=Status.COMPLETED, start_date=date.today(), end_date=date.today()
    )
    db_session.add(booking)
    db_session.commit()

    trip = Trip(booking_id=booking.booking_id, price=500.00)
    db_session.add(trip)
    db_session.commit()

    payment = Payment(
        trip_id=trip.trip_id, amount=500.00, 
        payment_type=PaymentType.CREDIT_CARD, 
        status=Status.COMPLETED,
        payment_date=datetime.now()
    )
    db_session.add(payment)
    db_session.commit()

    # 2. Запит на рейтинг
    response = client.get("/users/ranking")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    db_session.refresh(test_user)
    
    assert len(data) > 0
    assert data[0]["user_id"] == test_user.user_id
    assert float(data[0]["total_spent"]) == 500.0
    assert data[0]["rank"] == 1

def test_update_user_info(client, test_user):
    """Тест: Оновлення інформації про себе"""
    client.app.dependency_overrides[get_current_user] = lambda: test_user
    
    payload = {
        "firstname": "NewName",
        "lastname": "NewLastName"
    }
    response = client.patch("/users/me/update", json=payload)
    
    assert response.status_code == 200
    assert response.json()["firstname"] == "NewName"