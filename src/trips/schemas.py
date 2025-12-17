from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from src.models import CarStatus, FuelType

class CarSearchResponse(BaseModel):
    car_id: int
    license_plate: str
    model_name: str
    base_price: Decimal
    fuel_type: FuelType
    address: str
    status: CarStatus

model_config = {"from_attributes": True}

class TripFinishRequest(BaseModel):
    end_location_id: int = Field(..., description="ID локації, де ви залишили авто")

class TripResponse(BaseModel):
    trip_id: int
    start_time: datetime
    end_time: datetime | None
    price: Decimal | None
    start_location: int
    end_location: int | None

model_config = {"from_attributes": True}