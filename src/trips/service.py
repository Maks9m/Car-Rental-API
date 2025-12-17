from sqlalchemy.orm import Session
from src.trips.repository import TripRepository
from src.cars.repository import CarRepository
from src.models import FuelType, CarModel
from src.exceptions import BadRequest, NotFound
from decimal import Decimal

class TripService:
    def __init__(self):
        self.trip_repo = TripRepository()
        self.car_repo = CarRepository()

    # Simple Selects
    def search_available_cars(self, db: Session, location_id: int, max_price: float, fuel: FuelType):
        return self.car_repo.get_available_cars(db, location_id, max_price, fuel)

    # Delete Scenario
    def decommission_car(self, db: Session, car_id: int):
        if self.trip_repo.has_car_trips(db, car_id):
            raise BadRequest(detail="Cannot delete car: history of trips exists.")
        
        success = self.car_repo.hard_delete_car(db, car_id)
        if not success:
            raise NotFound(detail="Car not found")
        return {"message": "Car deleted"}

    # Update Scenario (НОВЕ)
    def update_model_price(self, db: Session, model_id: int, new_price: Decimal):
        model = db.query(CarModel).filter(CarModel.model_id == model_id).first()
        if not model:
            raise NotFound(detail="Car model not found")
        
        model.base_price = new_price
        db.commit()
        db.refresh(model)
        return model