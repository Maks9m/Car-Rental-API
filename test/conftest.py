
import pytest

from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from src.main import app
from src.database import get_db
from src.models import Base, Car, CarLocation, CarModel, CarStatus, DriverLicense, FuelType, LicenseType, User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

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