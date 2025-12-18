from sqlalchemy.orm import Session
from src.models import Trip, Booking

class TripRepository:
    def get_trip_by_id(self, db: Session, trip_id: int):
        return db.query(Trip).filter(Trip.trip_id == trip_id).first()

    def has_car_trips(self, db: Session, car_id: int) -> bool:

        trip_exists = db.query(Trip).join(Booking).filter(Booking.car_id == car_id).first()
        return trip_exists is not None