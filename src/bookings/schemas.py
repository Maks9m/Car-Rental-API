from datetime import date
from pydantic import BaseModel
from src.models import Status

class BookingBase(BaseModel):
    user_id: int
    car_id: int
    start_date: date
    end_date: date

class BookingResponse(BookingBase):
    booking_id: int
    status: Status

    model_config = {"from_attributes": True}

class BookingCreate(BookingBase):
    status: Status = Status.PENDING