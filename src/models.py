from sqlalchemy import String, DECIMAL, TIMESTAMP, Date, CHAR, ForeignKey, Enum, CheckConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date, datetime
from decimal import Decimal
from enum import Enum as PyEnum


class Base(DeclarativeBase):
    pass


# Enums
class LicenseType(str, PyEnum):
    M = "M"
    A = "A"
    A1 = "A1"
    B = "B"
    B1 = "B1"
    BE = "BE"
    C1 = "C1"
    D1 = "D1"

class FuelType(str, PyEnum):
    PETROL = "petrol"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"

class Status(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"

class CarStatus(str, PyEnum):
    AVAILABLE = "available"
    BOOKED = "booked"
    MAINTENANCE = "maintenance"
    UNAVAILABLE = "unavailable"

class PaymentType(str, PyEnum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"


# Models
class DriverLicense(Base):
    __tablename__ = "driver_license"

    driver_license_id: Mapped[int] = mapped_column(primary_key=True)
    license_number: Mapped[str] = mapped_column(CHAR(10), unique=True, nullable=False)
    license_type: Mapped[LicenseType] = mapped_column(Enum(LicenseType), nullable=False)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Relationships
    user: Mapped["User | None"] = relationship(back_populates="driver_license_rel", uselist=False)


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    driver_license_id: Mapped[int | None] = mapped_column(ForeignKey("driver_license.driver_license_id", ondelete="SET NULL"), index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(32), nullable=False)
    lastname: Mapped[str] = mapped_column(String(32), nullable=False)

    # Relationships
    driver_license_rel: Mapped["DriverLicense | None"] = relationship(back_populates="user")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="user_rel")


class CarLocation(Base):
    __tablename__ = "car_location"

    car_location_id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    cars: Mapped[list["Car"]] = relationship(back_populates="location_rel")
    trips_start: Mapped[list["Trip"]] = relationship(foreign_keys="Trip.start_location", back_populates="start_location_rel")
    trips_end: Mapped[list["Trip"]] = relationship(foreign_keys="Trip.end_location", back_populates="end_location_rel")


class CarModel(Base):
    __tablename__ = "car_model"

    model_id: Mapped[int] = mapped_column(primary_key=True)
    model_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    fuel_type: Mapped[FuelType] = mapped_column(Enum(FuelType), nullable=False)
    base_price: Mapped[Decimal] = mapped_column(DECIMAL(8, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("base_price > 0", name="check_base_price_positive"),
    )

    # Relationships
    cars: Mapped[list["Car"]] = relationship(back_populates="model_rel")


class Car(Base):
    __tablename__ = "car"

    car_id: Mapped[int] = mapped_column(primary_key=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("car_model.model_id", ondelete="RESTRICT"), nullable=False, index=True)
    location: Mapped[int | None] = mapped_column(ForeignKey("car_location.car_location_id", ondelete="SET NULL"), index=True)
    license_plate: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    status: Mapped[CarStatus] = mapped_column(Enum(CarStatus), nullable=False, index=True)

    # Relationships
    model_rel: Mapped["CarModel"] = relationship(back_populates="cars")
    location_rel: Mapped["CarLocation | None"] = relationship(back_populates="cars")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="car_rel")


class Booking(Base):
    __tablename__ = "booking"

    booking_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.user_id", ondelete="SET NULL"), index=True)
    car_id: Mapped[int | None] = mapped_column(ForeignKey("car.car_id", ondelete="SET NULL"), index=True)
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.PENDING, index=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="check_end_date_after_start_date"),
    )

    # Relationships
    user_rel: Mapped["User | None"] = relationship(back_populates="bookings")
    car_rel: Mapped["Car | None"] = relationship(back_populates="bookings")
    trips: Mapped[list["Trip"]] = relationship(back_populates="booking_rel")


class Trip(Base):
    __tablename__ = "trip"

    trip_id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int | None] = mapped_column(ForeignKey("booking.booking_id", ondelete="SET NULL"), index=True)
    start_location: Mapped[int | None] = mapped_column(ForeignKey("car_location.car_location_id", ondelete="SET NULL"), index=True)
    end_location: Mapped[int | None] = mapped_column(ForeignKey("car_location.car_location_id", ondelete="SET NULL"), index=True)
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now(), index=True)
    end_time: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    price: Mapped[Decimal | None] = mapped_column(DECIMAL(8, 2))

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_non_negative"),
    )

    # Relationships
    booking_rel: Mapped["Booking | None"] = relationship(back_populates="trips")
    start_location_rel: Mapped["CarLocation | None"] = relationship(foreign_keys=[start_location], back_populates="trips_start")
    end_location_rel: Mapped["CarLocation | None"] = relationship(foreign_keys=[end_location], back_populates="trips_end")
    payments: Mapped[list["Payment"]] = relationship(back_populates="trip_rel")


class Payment(Base):
    __tablename__ = "payment"

    payment_id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int | None] = mapped_column(ForeignKey("trip.trip_id", ondelete="SET NULL"), index=True)
    payment_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(8, 2), nullable=False)
    payment_type: Mapped[PaymentType | None] = mapped_column(Enum(PaymentType))
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.PENDING, index=True)

    __table_args__ = (
        CheckConstraint("amount > 0", name="check_amount_positive"),
    )

    # Relationships
    trip_rel: Mapped["Trip | None"] = relationship(back_populates="payments")
