from sqlalchemy.orm import Session
from src.models import Booking

class BookingRepository:
    def get_by_id(self, db: Session, booking_id: int) -> Booking | None:
        return db.query(Booking).filter(Booking.booking_id == booking_id).first()