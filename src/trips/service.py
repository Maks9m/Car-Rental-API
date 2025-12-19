from datetime import datetime
from decimal import Decimal
from src.trips.repository import TripRepository
from src.payments.repository import PaymentRepository
from src.models import CarStatus
from src.trips.exceptions import TripNotFound, TripAlreadyFinished, TripTransactionError

class TripService:
    def __init__(self):
        self.trip_repo = TripRepository()
        self.payment_repo = PaymentRepository()

    def finish_trip(self, db, trip_id, end_location_id):
        trip = self.trip_repo.get_trip_by_id(db, trip_id)
        if not trip:
            raise TripNotFound()
        if trip.end_time:
            raise TripAlreadyFinished()

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
            raise TripTransactionError(error_message=str(e))

    def list_trips(self, db):
        return self.trip_repo.get_all(db)