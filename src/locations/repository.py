from sqlalchemy import func
from sqlalchemy.orm import Session
from src.models import Location, Trip, Payment

class LocationRepository:
    def get_all(self, db: Session):
        return db.query(Location).all()

    def get_financial_report(self, db: Session):
        return db.query(
            Location.address.label("address"),
            func.count(Trip.trip_id).label("total_trips"),
            func.sum(Payment.amount).label("total_revenue"),
            func.avg(Payment.amount).label("avg_trip_cost")
        ).join(Trip, Location.location_id == Trip.end_location_id) \
         .join(Payment, Trip.trip_id == Payment.trip_id) \
         .group_by(Location.address) \
         .all()