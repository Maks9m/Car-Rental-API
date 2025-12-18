from sqlalchemy.orm import Session

from src.models import User, Status
from src.logger import log_execution

from src.auth.exceptions import UnauthorizedAction

from src.bookings.repository import BookingRepository
from src.bookings.exceptions import BookingNotFound, BookingUpdateNotAllowed, BookingClosed
from src.bookings.schemas import BookingBase, BookingCreate, BookingResponse, BookingUpdateDates

class BookingService:
    def __init__(self):
        self.booking_repo = BookingRepository()

    @log_execution
    def get_all_bookings(self, db: Session) -> list[BookingResponse]:
        return self.booking_repo.get_all(db)

    @log_execution
    def get_user_bookings(self, db: Session, user_id: int) -> list[BookingResponse]:
        return self.booking_repo.get_user_bookings(db, user_id)

    def create_booking(self, booking_data: BookingCreate, db: Session, current_user: User) -> BookingResponse:
        is_available = self.booking_repo.check_availability(
            db,
            booking_data.car_id,
            booking_data.start_date,
            booking_data.end_date
        )

        if not is_available:
            raise BookingUpdateNotAllowed(booking_data.car_id)
        
        return self.booking_repo.create(db, booking_data, current_user.user_id)
    
    @log_execution
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
    
    @log_execution
    def cancel_booking(self, db: Session, booking_id: int, current_user: User) -> BookingResponse:
        booking = self.booking_repo.get_by_id(db, booking_id)
        if not booking:
            raise BookingNotFound(booking_id)
        
        if booking.user_id != current_user.user_id:
            raise UnauthorizedAction()
        
        if booking.status != Status.PENDING:
            raise BookingClosed(booking_id)

        return self.booking_repo.cancel_booking(db, booking)
    
    @log_execution
    def confirm_booking(self, db: Session, booking_id: int) -> BookingResponse:
        booking = self.booking_repo.get_by_id(db, booking_id)
        if not booking:
            raise BookingNotFound(booking_id)
        
        if booking.status != Status.PENDING:
            raise BookingClosed(booking_id)
        
        return self.booking_repo.confirm_booking(db, booking)