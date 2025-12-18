from fastapi import APIRouter
from typing import List
from src.database import DB
from src.locations.service import LocationService
from src.locations.schemas import LocationAnalyticsResponse

router = APIRouter(prefix="/locations", tags=["Locations"])
service = LocationService()

@router.get("/analytics/revenue", response_model=List[LocationAnalyticsResponse])
def get_location_revenue_report(db: DB):
    return service.get_analytics(db)