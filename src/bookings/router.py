from fastapi import APIRouter, Depends
from src.database import DB
from src.bookings.service import BookingService
from src.bookings.schemas import BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])
service = BookingService()

@router.get("/{booking_id}")
def get_booking(booking_id: int, db: DB) -> BookingResponse:
    return service.get_booking_by_id(db, booking_id)