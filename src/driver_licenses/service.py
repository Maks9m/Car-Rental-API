
from datetime import date
from models import DriverLicense
from sqlalchemy.orm import Session
from src.driver_licenses.schemas import DriverLicenseResponse
from src.driver_licenses.exceptions import DriverLicenseNotFound
from src.driver_licenses.repository import DriverLicenseRepository

class DriverLicenseService:
    def __init__ (self):
        self.license_repo = DriverLicenseRepository()

    def get_driver_license_by_id(self, db: Session, license_id: int) -> DriverLicenseResponse | None:
        license = self.license_repo.get_by_id(db, license_id)
        if not license:
            raise DriverLicenseNotFound(license_id)
        return license

    def get_driver_license_by_number(self, db: Session, license_number: str) -> DriverLicenseResponse | None:
        license = self.license_repo.get_by_number(db, license_number)
        if not license:
            raise DriverLicenseNotFound(license_number)
        return license

    def is_license_expired(self, license: DriverLicense) -> bool:
        is_expired = license.expiry_date < date.today()
        if is_expired:
            return True
        return False
    