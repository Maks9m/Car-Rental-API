from sqlalchemy.orm import Session
from src.cars.repository import CarRepository
from src.trips.repository import TripRepository
from src.exceptions import BadRequest, NotFound

class CarService:
    def __init__(self):
        self.repo = CarRepository()
        self.trip_repo = TripRepository()

    def search_available_cars(self, db, location_id, max_price, fuel):
        return self.repo.get_available_cars(db, location_id, max_price, fuel)

    def decommission_car(self, db: Session, car_id: int):
        if self.trip_repo.has_car_trips(db, car_id):
            raise BadRequest(detail="Cannot delete car: history of trips exists.")
        if not self.repo.hard_delete_car(db, car_id):
            raise NotFound(detail="Car not found")
        db.commit()
        return {"message": "Car successfully deleted"}

    def update_model_price(self, db: Session, model_id: int, new_price):
        model = self.repo.get_model_by_id(db, model_id)
        if not model: raise NotFound(detail="Model not found")
        model.base_price = new_price
        db.commit()
        return model