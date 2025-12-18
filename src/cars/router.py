from fastapi import APIRouter, Query
from typing import List
from src.database import DB
from src.models import FuelType
from src.cars.service import CarService
from src.cars.schemas import CarSearchResponse, CarModelUpdate

router = APIRouter(prefix="/cars", tags=["Cars"])
service = CarService()

@router.get("/available", response_model=List[CarSearchResponse])
def get_available(db: DB, loc: int = Query(None), price: float = Query(None), fuel: FuelType = Query(None)):
    return service.search_available_cars(db, loc, price, fuel)

@router.patch("/models/{model_id}")
def update_price(model_id: int, data: CarModelUpdate, db: DB):
    return service.update_model_price(db, model_id, data.base_price)

@router.delete("/{car_id}")
def delete_car(car_id: int, db: DB):
    return service.decommission_car(db, car_id)