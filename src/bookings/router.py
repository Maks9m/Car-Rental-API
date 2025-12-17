from fastapi import APIRouter, Depends
from src.models import User
from src.database import DB
from src.logger import log_execution
from src.auth.dependencies import get_current_user
from src.bookings.service import BookingService
from src.bookings.schemas import BookingResponse, BookingUpdateDates

router = APIRouter(prefix="/bookings", tags=["Bookings"])
service = BookingService()

@router.patch("/{booking_id}/dates", response_model=BookingResponse)
@log_execution
def update_booking_dates(booking_id: int, update_dates: BookingUpdateDates, db: DB, current_user: User = Depends(get_current_user)):
    return service.update_dates(db, booking_id, update_dates, current_user)

@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
@log_execution
def cancel_booking(booking_id: int, db: DB, current_user: User = Depends(get_current_user)):
    return service.cancel_booking(db, booking_id, current_user)