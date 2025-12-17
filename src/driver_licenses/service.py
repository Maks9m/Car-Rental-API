from datetime import date
from sqlalchemy.orm import Session

from src.models import DriverLicense
from src.logger import log_execution

from src.users.repository import UserRepository
from src.users.exceptions import UserNotFound

from src.driver_licenses.schemas import DriverLicenseResponse
from src.driver_licenses.exceptions import DriverLicenseNotFound
from src.driver_licenses.repository import DriverLicenseRepository

class DriverLicenseService:
    def __init__ (self):
        self.license_repo = DriverLicenseRepository()
        self.user_repo = UserRepository()

    @log_execution
    def get_driver_license_by_id(self, db: Session, license_id: int) -> DriverLicenseResponse | None:
        license = self.license_repo.get_by_id(db, license_id)
        if not license:
            raise DriverLicenseNotFound(license_id)
        return license

    @log_execution
    def get_driver_license_by_number(self, db: Session, license_number: str) -> DriverLicenseResponse | None:
        license = self.license_repo.get_by_number(db, license_number)
        if not license:
            raise DriverLicenseNotFound(license_number)
        return license
    
    @log_execution
    def get_user_driver_license(self, db: Session, user_id: int) -> DriverLicenseResponse | None:
        user = self.user_repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFound(user_id)
        
        license = user.driver_license_rel

        if not license:
            raise DriverLicenseNotFound(user.driver_license_id)
        
        return license

    @log_execution
    def is_license_expired(self, license: DriverLicense) -> bool:
        is_expired = license.expiry_date < date.today()
        if is_expired:
            return True
        return False
    