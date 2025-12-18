from pydantic import BaseModel

class LocationAnalyticsResponse(BaseModel):
    address: str
    total_trips: int
    total_revenue: float
    avg_trip_cost: float

    class Config:
        from_attributes = True