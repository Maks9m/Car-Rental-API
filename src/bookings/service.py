from sqlalchemy.orm import Session
from src.bookings.repository import BookingRepository
from src.bookings.exceptions import BookingNotFound
from src.bookings.schemas import BookingResponse

class BookingService:
    def __init__(self):
        self.booking_repo = BookingRepository()

    def get_booking_by_id(self, db: Session, booking_id: int) -> BookingResponse | None:
        booking = self.booking_repo.get_by_id(db, booking_id)
        if not booking:
            raise BookingNotFound(booking_id)
        return booking