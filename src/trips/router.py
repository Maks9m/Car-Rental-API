from fastapi import APIRouter, Query, status, HTTPException
from typing import List
from src.database import DB
from src.models import FuelType
from src.trips.service import TripService
from src.cars.schemas import CarSearchResponse, CarModelUpdate # Додай CarModelUpdate в cars/schemas.py

router = APIRouter(prefix="/trips", tags=["Trips"])
trip_service = TripService()

@router.get("/available-cars", response_model=List[CarSearchResponse])
def get_available_cars(db: DB, location_id: int = Query(None), max_price: float = Query(None), fuel: FuelType = Query(None)):
    return trip_service.search_available_cars(db, location_id, max_price, fuel)

@router.delete("/cars/{car_id}")
def delete_car(car_id: int, db: DB):
    return trip_service.decommission_car(db, car_id)

@router.patch("/models/{model_id}")
def update_price(model_id: int, data: CarModelUpdate, db: DB):
    return trip_service.update_model_price(db, model_id, data.base_price)