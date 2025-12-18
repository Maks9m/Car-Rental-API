from pydantic import BaseModel

class LocationAnalyticsResponse(BaseModel):
    address: str
    total_trips: int
    total_revenue: float
    avg_trip_cost: float

    class Config:
        from_attributes = True

class LocationResponse(BaseModel):
    location_id: int
    address: str
    city: str | None

    class Config:
        from_attributes = True