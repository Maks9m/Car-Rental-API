from datetime import date
from pydantic import BaseModel, field_validator

from src.models import Status

class BookingBase(BaseModel):
    start_date: date
    end_date: date

    @field_validator('start_date', 'end_date')
    def date_must_be_future(cls, v):
        if v and v < date.today():
            raise ValueError("Dates cannot be in the past")
        return v

class BookingResponse(BookingBase):
    booking_id: int
    user_id: int
    car_id: int
    status: Status

    model_config = {"from_attributes": True}

class BookingCreate(BookingBase):
    car_id: int

class BookingUpdateDates(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    car_id: int

    @field_validator('start_date', 'end_date')
    def date_must_be_future(cls, v):
        if v and v < date.today():
            raise ValueError("Dates cannot be in the past")
        return v