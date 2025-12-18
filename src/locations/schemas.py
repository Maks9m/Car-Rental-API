from pydantic import BaseModel

class LocationAnalyticsResponse(BaseModel):
    address: str
    total_trips: int
    total_revenue: float
    avg_trip_cost: float

    model_config = {"from_attributes": True}

class LocationResponse(BaseModel):
    car_location_id: int
    address: str

    model_config = {"from_attributes": True}