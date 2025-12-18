from fastapi import APIRouter
from src.database import DB
from src.trips.service import TripService
from src.trips.schemas import TripFinishRequest, TripResponse

router = APIRouter(prefix="/trips", tags=["Trips"])
service = TripService()

@router.post("/{trip_id}/finish", response_model=TripResponse)
def finish(trip_id: int, data: TripFinishRequest, db: DB):
    return service.finish_trip(db, trip_id, data.end_location_id)
