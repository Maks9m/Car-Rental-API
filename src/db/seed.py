from datetime import date, datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from src.models import (
    DriverLicense, User, CarLocation, CarModel, Car, Booking, Trip, Payment,
    LicenseType, FuelType, Status, CarStatus, PaymentType
)


def seed_data(session: Session):
    """Seed the database with initial data."""
    
    # Check if data already exists
    if session.query(DriverLicense).first():
        print("Database already seeded. Skipping...")
        return
    
    # 1. Driver Licenses (12 rows)
    driver_licenses = [
        DriverLicense(license_number="DL10000001", license_type=LicenseType.B, expiry_date=date(2026, 1, 15)),
        DriverLicense(license_number="DL10000002", license_type=LicenseType.B, expiry_date=date(2027, 3, 22)),
        DriverLicense(license_number="DL10000003", license_type=LicenseType.A, expiry_date=date(2025, 11, 30)),
        DriverLicense(license_number="DL10000004", license_type=LicenseType.C1, expiry_date=date(2028, 7, 10)),
        DriverLicense(license_number="DL10000005", license_type=LicenseType.B, expiry_date=date(2026, 9, 5)),
        DriverLicense(license_number="DL10000006", license_type=LicenseType.B, expiry_date=date(2029, 2, 14)),
        DriverLicense(license_number="DL10000007", license_type=LicenseType.D1, expiry_date=date(2025, 12, 25)),
        DriverLicense(license_number="DL10000008", license_type=LicenseType.B, expiry_date=date(2027, 6, 18)),
        DriverLicense(license_number="DL10000009", license_type=LicenseType.BE, expiry_date=date(2030, 1, 1)),
        DriverLicense(license_number="DL10000010", license_type=LicenseType.B, expiry_date=date(2026, 4, 12)),
        DriverLicense(license_number="DL10000011", license_type=LicenseType.A, expiry_date=date(2028, 8, 30)),
        DriverLicense(license_number="DL10000012", license_type=LicenseType.B, expiry_date=date(2027, 10, 5)),
    ]
    session.add_all(driver_licenses)
    session.flush()  # Get IDs
    
    # 2. Users (12 rows)
    users = [
        User(email="john.doe@example.com", firstname="John", lastname="Doe", driver_license_id=driver_licenses[0].driver_license_id),
        User(email="jane.smith@example.com", firstname="Jane", lastname="Smith", driver_license_id=driver_licenses[1].driver_license_id),
        User(email="mike.jones@example.com", firstname="Mike", lastname="Jones", driver_license_id=driver_licenses[2].driver_license_id),
        User(email="sarah.connor@example.com", firstname="Sarah", lastname="Connor", driver_license_id=driver_licenses[3].driver_license_id),
        User(email="bruce.wayne@example.com", firstname="Bruce", lastname="Wayne", driver_license_id=driver_licenses[4].driver_license_id),
        User(email="clark.kent@example.com", firstname="Clark", lastname="Kent", driver_license_id=driver_licenses[5].driver_license_id),
        User(email="diana.prince@example.com", firstname="Diana", lastname="Prince", driver_license_id=driver_licenses[6].driver_license_id),
        User(email="peter.parker@example.com", firstname="Peter", lastname="Parker", driver_license_id=driver_licenses[7].driver_license_id),
        User(email="tony.stark@example.com", firstname="Tony", lastname="Stark", driver_license_id=driver_licenses[8].driver_license_id),
        User(email="natasha.romanoff@example.com", firstname="Natasha", lastname="Romanoff", driver_license_id=driver_licenses[9].driver_license_id),
        User(email="steve.rogers@example.com", firstname="Steve", lastname="Rogers", driver_license_id=driver_licenses[10].driver_license_id),
        User(email="wanda.maximoff@example.com", firstname="Wanda", lastname="Maximoff", driver_license_id=driver_licenses[11].driver_license_id),
    ]
    session.add_all(users)
    session.flush()
    
    # 3. Car Locations (12 rows)
    car_locations = [
        CarLocation(address="123 Main St, New York, NY"),
        CarLocation(address="456 Elm St, Los Angeles, CA"),
        CarLocation(address="789 Oak St, Chicago, IL"),
        CarLocation(address="101 Pine St, Houston, TX"),
        CarLocation(address="202 Maple St, Phoenix, AZ"),
        CarLocation(address="303 Cedar St, Philadelphia, PA"),
        CarLocation(address="404 Birch St, San Antonio, TX"),
        CarLocation(address="505 Walnut St, San Diego, CA"),
        CarLocation(address="606 Ash St, Dallas, TX"),
        CarLocation(address="707 Cherry St, San Jose, CA"),
        CarLocation(address="808 Spruce St, Austin, TX"),
        CarLocation(address="909 Fir St, Jacksonville, FL"),
    ]
    session.add_all(car_locations)
    session.flush()
    
    # 4. Car Models (12 rows)
    car_models = [
        CarModel(model_name="Toyota Corolla", fuel_type=FuelType.PETROL, base_price=Decimal("50.00")),
        CarModel(model_name="Honda Civic", fuel_type=FuelType.PETROL, base_price=Decimal("55.00")),
        CarModel(model_name="Tesla Model 3", fuel_type=FuelType.ELECTRIC, base_price=Decimal("80.00")),
        CarModel(model_name="Ford Mustang", fuel_type=FuelType.PETROL, base_price=Decimal("90.00")),
        CarModel(model_name="Chevrolet Bolt", fuel_type=FuelType.ELECTRIC, base_price=Decimal("70.00")),
        CarModel(model_name="Toyota Prius", fuel_type=FuelType.HYBRID, base_price=Decimal("60.00")),
        CarModel(model_name="BMW 3 Series", fuel_type=FuelType.DIESEL, base_price=Decimal("85.00")),
        CarModel(model_name="Audi A4", fuel_type=FuelType.DIESEL, base_price=Decimal("88.00")),
        CarModel(model_name="Nissan Leaf", fuel_type=FuelType.ELECTRIC, base_price=Decimal("65.00")),
        CarModel(model_name="Hyundai Elantra", fuel_type=FuelType.HYBRID, base_price=Decimal("52.00")),
        CarModel(model_name="Kia Forte", fuel_type=FuelType.PETROL, base_price=Decimal("48.00")),
        CarModel(model_name="Mercedes C-Class", fuel_type=FuelType.DIESEL, base_price=Decimal("95.00")),
    ]
    session.add_all(car_models)
    session.flush()
    
    # 5. Cars (12 rows)
    cars = [
        Car(model_id=car_models[0].model_id, location=car_locations[0].car_location_id, license_plate="ABC-1234", status=CarStatus.AVAILABLE),
        Car(model_id=car_models[1].model_id, location=car_locations[1].car_location_id, license_plate="DEF-5678", status=CarStatus.BOOKED),
        Car(model_id=car_models[2].model_id, location=car_locations[2].car_location_id, license_plate="GHI-9012", status=CarStatus.AVAILABLE),
        Car(model_id=car_models[3].model_id, location=car_locations[3].car_location_id, license_plate="JKL-3456", status=CarStatus.MAINTENANCE),
        Car(model_id=car_models[4].model_id, location=car_locations[4].car_location_id, license_plate="MNO-7890", status=CarStatus.AVAILABLE),
        Car(model_id=car_models[5].model_id, location=car_locations[5].car_location_id, license_plate="PQR-1234", status=CarStatus.BOOKED),
        Car(model_id=car_models[6].model_id, location=car_locations[6].car_location_id, license_plate="STU-5678", status=CarStatus.AVAILABLE),
        Car(model_id=car_models[7].model_id, location=car_locations[7].car_location_id, license_plate="VWX-9012", status=CarStatus.AVAILABLE),
        Car(model_id=car_models[8].model_id, location=car_locations[8].car_location_id, license_plate="YZA-3456", status=CarStatus.BOOKED),
        Car(model_id=car_models[9].model_id, location=car_locations[9].car_location_id, license_plate="BCD-7890", status=CarStatus.AVAILABLE),
        Car(model_id=car_models[10].model_id, location=car_locations[10].car_location_id, license_plate="EFG-1234", status=CarStatus.MAINTENANCE),
        Car(model_id=car_models[11].model_id, location=car_locations[11].car_location_id, license_plate="HIJ-5678", status=CarStatus.AVAILABLE),
    ]
    session.add_all(cars)
    session.flush()
    
    # 6. Bookings (15 rows)
    bookings = [
        Booking(user_id=users[0].user_id, car_id=cars[0].car_id, status=Status.COMPLETED),
        Booking(user_id=users[1].user_id, car_id=cars[1].car_id, status=Status.PENDING),
        Booking(user_id=users[2].user_id, car_id=cars[2].car_id, status=Status.COMPLETED),
        Booking(user_id=users[3].user_id, car_id=cars[3].car_id, status=Status.PENDING),
        Booking(user_id=users[4].user_id, car_id=cars[4].car_id, status=Status.COMPLETED),
        Booking(user_id=users[5].user_id, car_id=cars[5].car_id, status=Status.PENDING),
        Booking(user_id=users[6].user_id, car_id=cars[6].car_id, status=Status.COMPLETED),
        Booking(user_id=users[7].user_id, car_id=cars[7].car_id, status=Status.COMPLETED),
        Booking(user_id=users[8].user_id, car_id=cars[8].car_id, status=Status.PENDING),
        Booking(user_id=users[9].user_id, car_id=cars[9].car_id, status=Status.COMPLETED),
        Booking(user_id=users[10].user_id, car_id=cars[10].car_id, status=Status.PENDING),
        Booking(user_id=users[11].user_id, car_id=cars[11].car_id, status=Status.COMPLETED),
        Booking(user_id=users[0].user_id, car_id=cars[2].car_id, status=Status.COMPLETED),
        Booking(user_id=users[1].user_id, car_id=cars[3].car_id, status=Status.COMPLETED),
        Booking(user_id=users[2].user_id, car_id=cars[4].car_id, status=Status.COMPLETED),
    ]
    session.add_all(bookings)
    session.flush()
    
    # 7. Trips (12 rows)
    trips = [
        Trip(book_id=bookings[0].book_id, start_location=car_locations[0].car_location_id, end_location=car_locations[1].car_location_id,
             start_time=datetime(2025, 11, 1, 10, 0, 0), end_time=datetime(2025, 11, 1, 12, 0, 0), price=Decimal("100.00")),
        Trip(book_id=bookings[2].book_id, start_location=car_locations[2].car_location_id, end_location=car_locations[3].car_location_id,
             start_time=datetime(2025, 11, 2, 14, 0, 0), end_time=datetime(2025, 11, 2, 16, 0, 0), price=Decimal("160.00")),
        Trip(book_id=bookings[4].book_id, start_location=car_locations[4].car_location_id, end_location=car_locations[5].car_location_id,
             start_time=datetime(2025, 11, 3, 9, 0, 0), end_time=datetime(2025, 11, 3, 11, 0, 0), price=Decimal("140.00")),
        Trip(book_id=bookings[6].book_id, start_location=car_locations[6].car_location_id, end_location=car_locations[7].car_location_id,
             start_time=datetime(2025, 11, 4, 13, 0, 0), end_time=datetime(2025, 11, 4, 15, 0, 0), price=Decimal("170.00")),
        Trip(book_id=bookings[7].book_id, start_location=car_locations[7].car_location_id, end_location=car_locations[8].car_location_id,
             start_time=datetime(2025, 11, 5, 8, 0, 0), end_time=datetime(2025, 11, 5, 10, 0, 0), price=Decimal("176.00")),
        Trip(book_id=bookings[9].book_id, start_location=car_locations[9].car_location_id, end_location=car_locations[10].car_location_id,
             start_time=datetime(2025, 11, 6, 15, 0, 0), end_time=datetime(2025, 11, 6, 17, 0, 0), price=Decimal("104.00")),
        Trip(book_id=bookings[11].book_id, start_location=car_locations[11].car_location_id, end_location=car_locations[0].car_location_id,
             start_time=datetime(2025, 11, 7, 11, 0, 0), end_time=datetime(2025, 11, 7, 13, 0, 0), price=Decimal("190.00")),
        Trip(book_id=bookings[1].book_id, start_location=car_locations[1].car_location_id, end_location=car_locations[2].car_location_id,
             start_time=datetime(2025, 11, 8, 10, 0, 0), end_time=None, price=Decimal("110.00")),
        Trip(book_id=bookings[5].book_id, start_location=car_locations[5].car_location_id, end_location=car_locations[6].car_location_id,
             start_time=datetime(2025, 11, 9, 12, 0, 0), end_time=None, price=Decimal("120.00")),
        Trip(book_id=bookings[8].book_id, start_location=car_locations[8].car_location_id, end_location=car_locations[9].car_location_id,
             start_time=datetime(2025, 11, 10, 14, 0, 0), end_time=None, price=Decimal("130.00")),
        Trip(book_id=bookings[12].book_id, start_location=car_locations[2].car_location_id, end_location=car_locations[0].car_location_id,
             start_time=datetime(2025, 11, 12, 8, 0, 0), end_time=datetime(2025, 11, 12, 9, 0, 0), price=Decimal("80.00")),
        Trip(book_id=bookings[13].book_id, start_location=car_locations[3].car_location_id, end_location=car_locations[1].car_location_id,
             start_time=datetime(2025, 11, 13, 10, 0, 0), end_time=datetime(2025, 11, 13, 11, 0, 0), price=Decimal("90.00")),
    ]
    session.add_all(trips)
    session.flush()
    
    # 8. Payments (12 rows)
    payments = [
        Payment(trip_id=trips[0].trip_id, payment_date=datetime(2025, 11, 1, 12, 5, 0), amount=Decimal("100.00"), payment_type=PaymentType.CREDIT_CARD, status=Status.COMPLETED),
        Payment(trip_id=trips[1].trip_id, payment_date=datetime(2025, 11, 2, 16, 5, 0), amount=Decimal("160.00"), payment_type=PaymentType.DEBIT_CARD, status=Status.COMPLETED),
        Payment(trip_id=trips[2].trip_id, payment_date=datetime(2025, 11, 3, 11, 5, 0), amount=Decimal("140.00"), payment_type=PaymentType.CREDIT_CARD, status=Status.COMPLETED),
        Payment(trip_id=trips[3].trip_id, payment_date=datetime(2025, 11, 4, 15, 5, 0), amount=Decimal("170.00"), payment_type=PaymentType.PAYPAL, status=Status.COMPLETED),
        Payment(trip_id=trips[4].trip_id, payment_date=datetime(2025, 11, 5, 10, 5, 0), amount=Decimal("176.00"), payment_type=PaymentType.DEBIT_CARD, status=Status.COMPLETED),
        Payment(trip_id=trips[5].trip_id, payment_date=datetime(2025, 11, 6, 17, 5, 0), amount=Decimal("104.00"), payment_type=PaymentType.CREDIT_CARD, status=Status.COMPLETED),
        Payment(trip_id=trips[6].trip_id, payment_date=datetime(2025, 11, 7, 13, 5, 0), amount=Decimal("190.00"), payment_type=PaymentType.CREDIT_CARD, status=Status.COMPLETED),
        Payment(trip_id=trips[7].trip_id, payment_date=datetime(2025, 11, 8, 10, 5, 0), amount=Decimal("110.00"), payment_type=PaymentType.DEBIT_CARD, status=Status.PENDING),
        Payment(trip_id=trips[8].trip_id, payment_date=datetime(2025, 11, 9, 12, 5, 0), amount=Decimal("120.00"), payment_type=PaymentType.CREDIT_CARD, status=Status.PENDING),
        Payment(trip_id=trips[9].trip_id, payment_date=datetime(2025, 11, 10, 14, 5, 0), amount=Decimal("130.00"), payment_type=PaymentType.PAYPAL, status=Status.PENDING),
        Payment(trip_id=trips[10].trip_id, payment_date=datetime(2025, 11, 12, 9, 5, 0), amount=Decimal("80.00"), payment_type=PaymentType.CREDIT_CARD, status=Status.COMPLETED),
        Payment(trip_id=trips[11].trip_id, payment_date=datetime(2025, 11, 13, 11, 5, 0), amount=Decimal("90.00"), payment_type=PaymentType.DEBIT_CARD, status=Status.COMPLETED),
    ]
    session.add_all(payments)
    
    # Commit all changes
    session.commit()
    print("Database seeded successfully!")


def run_seed():
    from src.db.session import SessionLocal
    
    session = SessionLocal()
    try:
        seed_data(session)
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run_seed()
