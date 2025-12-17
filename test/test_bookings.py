import pytest
from datetime import date, timedelta
from fastapi import status
from src.models import Booking, Car, CarModel, CarLocation, DriverLicense, User, Status, LicenseType, FuelType, CarStatus
from src.auth.dependencies import get_current_user

# --- Fixtures для створення тестових даних ---

@pytest.fixture
def test_user(db_session):
    """Створює тестового користувача"""
    license = DriverLicense(
        license_number="D1234567",
        license_type=LicenseType.B,
        expiry_date=date.today() + timedelta(days=365 * 3)
    )
    db_session.add(license)
    db_session.commit()
    db_session.refresh(license)

    user = User(
        email="renter@example.com",
        firstname="Renter",
        lastname="Test",
        password_hash="hashed_secret",
        driver_license_id=license.driver_license_id
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def another_user(db_session):
    """Створює іншого користувача (для перевірки прав доступу)"""
    license = DriverLicense(
        license_number="D0123456",
        license_type=LicenseType.B,
        expiry_date=date.today() + timedelta(days=365 * 3)
    )
    db_session.add(license)
    db_session.commit()
    db_session.refresh(license)

    user = User(
        email="other@example.com",
        firstname="Other",
        lastname="Person",
        password_hash="hashed_secret",
        driver_license_id=license.driver_license_id
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_car(db_session):
    """Створює тестове авто"""
    # Спочатку потрібні Location та Model
    loc = CarLocation(address="Test St 1")
    db_session.add(loc)
    
    model = CarModel(
        model_name="Tesla Model S", 
        fuel_type=FuelType.ELECTRIC, 
        base_price=100.00
    )
    db_session.add(model)
    db_session.commit()
    db_session.refresh(loc)
    db_session.refresh(model)

    car = Car(
        model_id=model.model_id,
        location=loc.car_location_id,
        license_plate="TESLA001",
        status=CarStatus.AVAILABLE
    )
    db_session.add(car)
    db_session.commit()
    db_session.refresh(car)
    return car

# --- Тести ---

def test_update_booking_dates_success(client, db_session, test_user, test_car):
    """Тест: Успішна зміна дат бронювання"""
    # 1. Створюємо бронювання (10-15 число)
    booking = Booking(
        user_id=test_user.user_id,
        car_id=test_car.car_id,
        start_date=date.today() + timedelta(days=10),
        end_date=date.today() + timedelta(days=15),
        status=Status.PENDING
    )
    db_session.add(booking)
    db_session.commit()

    # 2. Підміняємо аутентифікацію (ми залогінені як test_user)
    client.app.dependency_overrides[get_current_user] = lambda: test_user

    # 3. Відправляємо запит на зміну дат (12-14 число)
    new_start = date.today() + timedelta(days=12)
    new_end = date.today() + timedelta(days=14)
    
    payload = {
        "start_date": new_start.isoformat(),
        "end_date": new_end.isoformat(),
        "car_id": test_car.car_id # Твоя схема вимагає це поле
    }

    response = client.put(f"/bookings/{booking.booking_id}/dates", json=payload)

    # 4. Перевірка
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["start_date"] == new_start.isoformat()
    assert data["end_date"] == new_end.isoformat()

def test_update_booking_dates_conflict(client, db_session, test_user, test_car):
    """Тест: Спроба змінити дати на зайняті (Conflict)"""
    # Бронювання 1 (Користувач А): 10-15 число (Те, що ми міняємо)
    booking1 = Booking(
        user_id=test_user.user_id,
        car_id=test_car.car_id,
        start_date=date.today() + timedelta(days=10),
        end_date=date.today() + timedelta(days=15),
        status=Status.PENDING
    )
    
    # Бронювання 2 (Користувач Б): 20-25 число (Заважає змінам)
    booking2 = Booking(
        user_id=test_user.user_id, # Може бути той самий юзер
        car_id=test_car.car_id,
        start_date=date.today() + timedelta(days=20),
        end_date=date.today() + timedelta(days=25),
        status=Status.PENDING
    )
    db_session.add_all([booking1, booking2])
    db_session.commit()

    client.app.dependency_overrides[get_current_user] = lambda: test_user

    # Спробуємо змінити Booking 1 так, щоб він наліз на Booking 2 (18-22 число)
    payload = {
        "start_date": (date.today() + timedelta(days=18)).isoformat(),
        "end_date": (date.today() + timedelta(days=22)).isoformat(),
        "car_id": test_car.car_id
    }

    response = client.put(f"/bookings/{booking1.booking_id}/dates", json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "not available" in response.json()["detail"]

def test_cancel_booking_success(client, db_session, test_user, test_car):
    """Тест: Успішне скасування бронювання"""
    booking = Booking(
        user_id=test_user.user_id,
        car_id=test_car.car_id,
        start_date=date.today() + timedelta(days=5),
        end_date=date.today() + timedelta(days=6),
        status=Status.PENDING
    )
    db_session.add(booking)
    db_session.commit()

    client.app.dependency_overrides[get_current_user] = lambda: test_user

    response = client.put(f"/bookings/{booking.booking_id}/cancel")

    assert response.status_code == status.HTTP_200_OK
    # Перевіряємо, що статус змінився. 
    # Примітка: перевір, чи повертає API 'canceled' або 'CANCELLED' залежно від твого Enum/Repo
    assert response.json()["status"].upper() in ["CANCELED", "CANCELLED"] 

def test_cancel_booking_not_owner(client, db_session, test_user, another_user, test_car):
    """Тест: Спроба скасувати чуже бронювання"""
    booking = Booking(
        user_id=another_user.user_id, # Власник - інший юзер
        car_id=test_car.car_id,
        start_date=date.today() + timedelta(days=5),
        end_date=date.today() + timedelta(days=6),
        status=Status.PENDING
    )
    db_session.add(booking)
    db_session.commit()

    # Ми залогінені як test_user, а бронювання належить another_user
    client.app.dependency_overrides[get_current_user] = lambda: test_user

    response = client.put(f"/bookings/{booking.booking_id}/cancel")

    # Очікуємо 401 або 403 залежно від того, що кидає UnauthorizedAction
    assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

def test_update_closed_booking(client, db_session, test_user, test_car):
    """Тест: Спроба змінити вже скасоване бронювання"""
    booking = Booking(
        user_id=test_user.user_id,
        car_id=test_car.car_id,
        start_date=date.today() + timedelta(days=5),
        end_date=date.today() + timedelta(days=6),
        # Статус не PENDING
        status=Status.CANCELED 
    )
    db_session.add(booking)
    db_session.commit()

    client.app.dependency_overrides[get_current_user] = lambda: test_user

    payload = {
        "start_date": (date.today() + timedelta(days=7)).isoformat(),
        "end_date": (date.today() + timedelta(days=8)).isoformat(),
        "car_id": test_car.car_id
    }

    response = client.put(f"/bookings/{booking.booking_id}/dates", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "closed" in response.json()["detail"]