from sqlalchemy import func
from sqlalchemy.orm import Session
from src.models import CarLocation, Trip, Payment

class LocationRepository:
    def get_all(self, db: Session):
        return db.query(CarLocation).all()

    def get_financial_report(self, db: Session):
        return db.query(
            CarLocation.address.label("address"),
            func.count(Trip.trip_id).label("total_trips"),
            func.sum(Payment.amount).label("total_revenue"),
            func.avg(Payment.amount).label("avg_trip_cost")
        ).join(Trip, CarLocation.CarLocation_id == Trip.end_CarLocation_id) \
         .join(Payment, Trip.trip_id == Payment.trip_id) \
         .group_by(CarLocation.address) \
         .all()