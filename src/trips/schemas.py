from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

class TripFinishRequest(BaseModel):
    end_location_id: int = Field(..., description="ID локації завершення поїздки")

class TripResponse(BaseModel):
    trip_id: int
    start_time: datetime
    end_time: datetime | None
    price: Decimal | None
    status: str = "COMPLETED"

    model_config = {"from_attributes": True}

class TripFinishRequest(BaseModel):
    end_location_id: int = Field(..., description="ID локації, де користувач залишив авто")