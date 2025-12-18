from fastapi import APIRouter, Depends, status

from src.models import User
from src.database import DB
from src.logger import log_execution

from src.auth.dependencies import get_current_user

from src.bookings.service import BookingService
from src.bookings.schemas import BookingCreate, BookingResponse, BookingUpdateDates

router = APIRouter(prefix="/bookings", tags=["Bookings"])
service = BookingService()

@router.get("", response_model=list[BookingResponse])
@log_execution
def get_all_bookings(db: DB):
    return service.get_all_bookings(db)

@router.get("/me", response_model=list[BookingResponse])
@log_execution
def get_user_bookings(db: DB, current_user: User = Depends(get_current_user)):
    return service.get_user_bookings(db, current_user.user_id)

@router.post("/create", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking_data: BookingCreate, db: DB, current_user: User = Depends(get_current_user)):
    return service.create_booking(booking_data,db, current_user)

@router.patch("/{booking_id}/dates", response_model=BookingResponse)
@log_execution
def update_booking_dates(booking_id: int, update_dates: BookingUpdateDates, db: DB, current_user: User = Depends(get_current_user)):
    return service.update_dates(db, booking_id, update_dates, current_user)

@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
@log_execution
def cancel_booking(booking_id: int, db: DB, current_user: User = Depends(get_current_user)):
    return service.cancel_booking(db, booking_id, current_user)