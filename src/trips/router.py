from fastapi import APIRouter, Query, Depends
from src.database import DB
from src.models import FuelType
from src.trips.service import TripService
from src.trips.schemas import CarSearchResponse, TripResponse, TripFinishRequest
from typing import List

router = APIRouter(prefix="/trips", tags=["Trips"])
service = TripService()

@router.get("/available-cars", response_model=List[CarSearchResponse])
def search_cars(
    db: DB,
    location_id: int = Query(None),
    max_price: float = Query(None),
    fuel: FuelType = Query(None)
):
    return service.get_available_cars_for_trip(db, location_id, max_price, fuel)

@router.post("/{trip_id}/finish", response_model=TripResponse)
def finish_trip(trip_id: int, data: TripFinishRequest, db: DB):
    return service.finish_trip(db, trip_id, data.end_location_id)