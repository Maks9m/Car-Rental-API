from sqlalchemy.orm import Session
from src.models import Car, CarModel, CarLocation, CarStatus, FuelType

class CarRepository:
    def get_available_cars(
        self, 
        db: Session, 
        location_id: int = None, 
        max_price: float = None, 
        fuel: FuelType = None
    ):
        query = db.query(
            Car.car_id,
            Car.license_plate,
            Car.status,
            CarModel.model_name,
            CarModel.fuel_type,
            CarModel.base_price,
            CarLocation.address
        ).join(CarModel, Car.model_id == CarModel.model_id)\
         .join(CarLocation, Car.location == CarLocation.car_location_id)

        query = query.filter(Car.status == CarStatus.AVAILABLE)

        if location_id:
            query = query.filter(Car.location == location_id)
        if max_price:
            query = query.filter(CarModel.base_price <= max_price)
        if fuel:
            query = query.filter(CarModel.fuel_type == fuel)

        return query.all()

    def hard_delete_car(self, db: Session, car_id: int):
        car = db.query(Car).filter(Car.car_id == car_id).first()
        if car:
            db.delete(car)
            db.commit()
            return True
        return False