from sqlalchemy.orm import Session
from src.models import User, Status
from src.auth.exceptions import UnauthorizedAction
from src.bookings.repository import BookingRepository
from src.bookings.exceptions import BookingNotFound, BookingUpdateNotAllowed, BookingClosed
from src.bookings.schemas import BookingBase, BookingResponse, BookingUpdateDates

class BookingService:
    def __init__(self):
        self.booking_repo = BookingRepository()
    
    def update_dates(self, db: Session, booking_id: int, update_data: BookingUpdateDates, current_user: User) -> BookingResponse:

        booking = self.booking_repo.get_by_id(db, booking_id)
        if not booking:
            raise BookingNotFound(booking_id)
        
        if booking.user_id != current_user.user_id:
            raise UnauthorizedAction()
        
        if booking.status != Status.PENDING:
            raise BookingClosed(booking_id)
        
        new_dates = BookingBase(
            start_date=update_data.start_date or booking.start_date,
            end_date=update_data.end_date or booking.end_date
        )

        is_available = self.booking_repo.check_availability(
            db,
            booking.car_id,
            new_dates.start_date,
            new_dates.end_date,
            booking.booking_id
        )

        if not is_available:
            raise BookingUpdateNotAllowed(booking.car_id)
        
        return self.booking_repo.update_dates(db, booking, new_dates)
    
    def cancel_booking(self, db: Session, booking_id: int, current_user: User) -> BookingResponse:
        booking = self.booking_repo.get_by_id(db, booking_id)
        if not booking:
            raise BookingNotFound(booking_id)
        
        if booking.user_id != current_user.user_id:
            raise UnauthorizedAction()
        
        if booking.status != Status.PENDING:
            raise BookingClosed(booking_id)

        return self.booking_repo.cancel_booking(db, booking)
    
    def confirm_booking(self, db: Session, booking_id: int) -> BookingResponse:
        booking = self.booking_repo.get_by_id(db, booking_id)
        if not booking:
            raise BookingNotFound(booking_id)
        
        if booking.status != Status.PENDING:
            raise BookingClosed(booking_id)
        
        return self.booking_repo.confirm_booking(db, booking)