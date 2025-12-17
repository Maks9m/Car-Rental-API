from sqlalchemy.orm import Session
from src.models import DriverLicense
from src.logger import log_execution
from src.driver_licenses.schemas import DriverLicenseCreate

class DriverLicenseRepository:
    def get_by_id(self, db: Session, license_id: int) -> DriverLicense | None:
        return db.query(DriverLicense).filter(DriverLicense.driver_license_id == license_id).first()
    
    def get_by_number(self, db: Session, license_number: str) -> DriverLicense | None:
        return db.query(DriverLicense).filter(DriverLicense.license_number == license_number).first()
    
    @log_execution
    def create(self, db: Session, license_data: DriverLicenseCreate) -> DriverLicense:
        new_license = DriverLicense(
            license_number=license_data.license_number,
            license_type=license_data.license_type,
            expiry_date=license_data.expiry_date
        )
        db.add(new_license)
        db.flush()
        return new_license