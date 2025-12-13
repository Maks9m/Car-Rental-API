
from datetime import date
from models import DriverLicense
from sqlalchemy.orm import Session
from src.driver_licenses.schemas import DriverLicenseResponse
from src.driver_licenses.exceptions import DriverLicenseNotFound


def get_driver_license_by_id(db: Session, license_id: int) -> DriverLicenseResponse | None:
    license =db.query(DriverLicense).filter(DriverLicense.driver_license_id == license_id).first()
    if not license:
        raise DriverLicenseNotFound(license_id)
    return license

def get_driver_license_by_number(db: Session, license_number: str) -> DriverLicenseResponse | None:
    license = db.query(DriverLicense).filter(DriverLicense.license_number == license_number).first()
    return license

def is_license_expired(license: DriverLicense) -> bool:
    is_expired = license.expiry_date < date.today()
    if is_expired:
        return True
    return False