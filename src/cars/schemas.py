from pydantic import BaseModel, Field, field_validator
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
        

class CarModelUpdate(BaseModel):
    base_price: Decimal = Field(..., ge=0.1)

    @field_validator('base_price')
    @classmethod
    def validate_price(cls, v):
        if v > 1000000:
            raise ValueError('Price is too high')
        return v