import random
from datetime import timedelta
from decimal import Decimal
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import text

# Імпортуємо твої моделі та налаштування БД
# Переконайся, що імпорти відповідають твоїй структурі папок
from src.database import SessionLocal, engine
from src.models import (
    DriverLicense, User, CarLocation, CarModel, Car, Booking, Trip, Payment,
    LicenseType, FuelType, Status, CarStatus, PaymentType
)

fake = Faker()

# Налаштування кількості даних
NUM_USERS = 50
NUM_LOCATIONS = 10
NUM_MODELS = 10
NUM_CARS = 30
NUM_BOOKINGS = 100

def reset_database(session: Session):
    """Очищає таблиці перед наповненням (Опціонально)"""
    print("Cleaning database...")
    # Вимикаємо перевірку зовнішніх ключів для швидкого видалення (Postgres/SQLite)
    try:
        session.execute(text("TRUNCATE TABLE payment, trip, booking, car, car_model, car_location, \"user\", driver_license RESTART IDENTITY CASCADE;"))
    except Exception:
        # Fallback для SQLite (якщо використовуєш його)
        session.execute(text("DELETE FROM payment;"))
        session.execute(text("DELETE FROM trip;"))
        session.execute(text("DELETE FROM booking;"))
        session.execute(text("DELETE FROM car;"))
        session.execute(text("DELETE FROM car_model;"))
        session.execute(text("DELETE FROM car_location;"))
        session.execute(text("DELETE FROM \"user\";"))
        session.execute(text("DELETE FROM driver_license;"))
    session.commit()

def create_driver_license():
    return DriverLicense(
        license_number=fake.unique.bothify(text='DL########'),
        license_type=random.choice(list(LicenseType)),
        expiry_date=fake.date_between(start_date='+1y', end_date='+10y')
    )

def create_user(license_id):
    return User(
        email=fake.unique.email(),
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        password_hash="hashed_secret_password", # У реальності тут має бути хеш
        driver_license_id=license_id
    )

def create_locations():
    locations = []
    for _ in range(NUM_LOCATIONS):
        locations.append(CarLocation(address=fake.address()))
    return locations

def create_models():
    models = []
    car_names = ["Toyota Corolla", "Honda Civic", "Tesla Model 3", "Ford Mustang", "BMW 3", "Audi A4", "VW Golf", "Kia Sportage"]
    for _ in range(NUM_MODELS):
        models.append(CarModel(
            model_name=f"{random.choice(car_names)} {fake.unique.random_int(1, 999)}",
            fuel_type=random.choice(list(FuelType)),
            base_price=Decimal(random.randint(40, 150))
        ))
    return models

def seed_data(session: Session):
    # 0. Очистка (розкоментуй, якщо хочеш завжди чисту базу)
    # reset_database(session)

    # Перевірка, чи база вже заповнена
    if session.query(User).count() > 0:
        print("Database already contains data. Skipping seed.")
        return

    print("Seeding Users and Licenses...")
    users = []
    for _ in range(NUM_USERS):
        # 1. Створюємо ліцензію
        lic = create_driver_license()
        session.add(lic)
        session.flush() # Щоб отримати ID
        
        # 2. Створюємо юзера
        user = create_user(lic.driver_license_id)
        session.add(user)
        users.append(user)
    
    print("Seeding Locations and Models...")
    locations = create_locations()
    session.add_all(locations)
    
    models = create_models()
    session.add_all(models)
    session.flush()

    print("Seeding Cars...")
    cars = []
    for _ in range(NUM_CARS):
        car = Car(
            model_id=random.choice(models).model_id,
            location=random.choice(locations).car_location_id,
            license_plate=fake.unique.license_plate(),
            status=random.choice(list(CarStatus))
        )
        cars.append(car)
    session.add_all(cars)
    session.flush()

    print("Seeding Bookings, Trips and Payments...")
    for _ in range(NUM_BOOKINGS):
        user = random.choice(users)
        car = random.choice(cars)
        
        # 1. Booking
        booking_status = random.choice(list(Status))
        booking = Booking(
            user_id=user.user_id,
            car_id=car.car_id,
            status=booking_status
            # Примітка: Якщо ти вже додав start_date/end_date у модель Booking, розкоментуй це:
            # start_date=fake.date_this_year(),
            # end_date=fake.date_this_year() + timedelta(days=random.randint(1, 5))
        )
        session.add(booking)
        session.flush()

        # 2. Trip (тільки якщо бронювання завершене або підтверджене)
        if booking_status in [Status.COMPLETED]:
            start_time = fake.date_time_this_year()
            end_time = start_time + timedelta(hours=random.randint(1, 48))
            
            trip = Trip(
                book_id=booking.book_id,
                start_location=car.location, # Беремо поточну локацію авто
                end_location=random.choice(locations).car_location_id,
                start_time=start_time,
                end_time=end_time,
                price=Decimal(random.randint(50, 500))
            )
            session.add(trip)
            session.flush()

            # 3. Payment (для кожної поїздки)
            payment = Payment(
                trip_id=trip.trip_id,
                payment_date=end_time + timedelta(minutes=5),
                amount=trip.price,
                payment_type=random.choice(list(PaymentType)),
                status=Status.COMPLETED
            )
            session.add(payment)

    session.commit()
    print("✅ Database seeded successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_data(db)
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()