from datetime import date

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.models import Booking, Status
from src.logger import log_execution

from src.bookings.schemas import BookingBase

class BookingRepository:
    def get_by_id(self, db: Session, booking_id: int) -> Booking | None:
        return db.query(Booking).filter(Booking.booking_id == booking_id).first()
    
    def get_all(self, db: Session) -> list[Booking]:
        return db.query(Booking).all()
    
    def get_user_bookings(self, db: Session, user_id: int) -> list[Booking]:
        return db.query(Booking).filter(Booking.user_id == user_id).all()
    
    @log_execution
    def create(self, db: Session, booking_data: BookingBase, user_id: int) -> Booking:
        new_booking = Booking(
            car_id=booking_data.car_id,
            user_id=user_id,
            start_date=booking_data.start_date,
            end_date=booking_data.end_date,
            status=Status.PENDING
        )

        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking
    
    @log_execution
    def update_dates(self, db: Session, booking: Booking, new_dates: BookingBase) -> Booking:
        if new_dates.start_date:
            booking.start_date = new_dates.start_date
        if new_dates.end_date:
            booking.end_date = new_dates.end_date

        db.commit()
        db.refresh(booking)
        return booking
    
    def check_availability(self, db: Session, car_id: int, start_date: date, end_date: date, exclude_booking_id: int | None = None) -> bool:
        query =db.query(Booking).filter(
                Booking.booking_id != exclude_booking_id,
                Booking.car_id == car_id,
                and_(
                    Booking.start_date < end_date,
                    Booking.end_date > start_date
                ),
                Booking.status != Status.CANCELED,
            )
        
        if exclude_booking_id is None:
            query = query.filter(Booking.booking_id != exclude_booking_id)

        overlapping_bookings = query.count()

        return overlapping_bookings == 0
    
    @log_execution
    def cancel_booking(self, db: Session, booking: Booking) -> Booking:
        booking.status = Status.CANCELED
        db.commit()
        db.refresh(booking)
        return booking
    
    @log_execution
    def complete_booking(self, db: Session, booking: Booking) -> Booking:
        booking.status = Status.COMPLETED
        db.commit()
        db.refresh(booking)
        return booking