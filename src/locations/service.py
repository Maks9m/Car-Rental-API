from src.locations.repository import LocationRepository

class LocationService:
    def __init__(self):
        self.repo = LocationRepository()

    def get_analytics(self, db):
        return self.repo.get_financial_report(db)