from datetime import datetime
from sqlalchemy.orm import Session
from src.trips.repository import TripRepository
from src.models import Trip, Payment, Car, CarStatus, Status, FuelType
from src.exceptions import NotFound, BadRequest

class TripService:
    def __init__(self):
        self.trip_repo = TripRepository()

    def get_available_cars_for_trip(
        self, 
        db: Session, 
        location_id: int = None, 
        max_price: float = None, 
        fuel: FuelType = None
    ):

        return self.trip_repo.get_available_cars(db, location_id, max_price, fuel)

    def finish_trip(self, db: Session, trip_id: int, end_location_id: int):
        trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
        if not trip:
            raise NotFound(detail="Trip not found")
        
        if trip.end_time:
            raise BadRequest(detail="Trip is already finished")

        end_time = datetime.now()
        duration = end_time - trip.start_time
        hours = max(1, duration.total_seconds() / 3600)

        try:
            base_price = trip.booking_rel.car_rel.model_rel.base_price
        except AttributeError:
            raise BadRequest(detail="Could not calculate price: Car model information missing")
            
        final_price = base_price * int(hours)

        try:
            trip.end_time = end_time
            trip.price = final_price
            trip.end_location = end_location_id

            new_payment = Payment(
                trip_id=trip.trip_id,
                amount=final_price,
                payment_date=end_time,
                status=Status.COMPLETED
            )
            db.add(new_payment)

            car = trip.booking_rel.car_rel
            car.status = CarStatus.AVAILABLE
            car.location = end_location_id

            db.commit() 
            db.refresh(trip)
            return trip
            
        except Exception as e:
            db.rollback() 
            raise BadRequest(detail=f"Transaction failed: {str(e)}")