from datetime import datetime
from decimal import Decimal
from src.trips.repository import TripRepository
from src.payments.repository import PaymentRepository
from src.models import CarStatus
from src.exceptions import BadRequest, NotFound

class TripService:
    def __init__(self):
        self.trip_repo = TripRepository()
        self.payment_repo = PaymentRepository()

    def finish_trip(self, db, trip_id, end_location_id):
        trip = self.trip_repo.get_trip_by_id(db, trip_id)
        if not trip or trip.end_time: raise BadRequest(detail="Invalid trip")

        car = trip.booking_rel.car_rel
        duration = datetime.now() - trip.start_time
        total_price = (Decimal(max(1, duration.total_seconds() / 60)) * (car.model_rel.base_price / 60)).quantize(Decimal("0.01"))

        try:
            trip.end_time, trip.end_location, trip.price = datetime.now(), end_location_id, total_price
            car.status, car.location = CarStatus.AVAILABLE, end_location_id
            self.payment_repo.create_pending_payment(db, trip.trip_id, total_price)
            db.commit()
            return trip
        except Exception as e:
            db.rollback()
            raise BadRequest(detail=str(e))