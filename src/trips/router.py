from fastapi import APIRouter
from src.database import DB
from src.trips.service import TripService
from src.trips.schemas import TripFinishRequest, TripResponse

router = APIRouter(prefix="/trips", tags=["Trips"])
service = TripService()

@router.post("/{trip_id}/finish", response_model=TripResponse)
def finish(trip_id: int, data: TripFinishRequest, db: DB):
    return service.finish_trip(db, trip_id, data.end_location_id)

from typing import List
from src.trips.schemas import TripResponse

@router.get("/", response_model=List[TripResponse])
def get_all_trips(db: DB):
    return service.list_trips(db)
