from fastapi import APIRouter, Depends

from src.logger import log_execution
from src.database import DB
from src.models import User

from src.driver_licenses.service import DriverLicenseService

from src.auth.dependencies import get_current_user

router = APIRouter(prefix="/driver-licenses", tags=["Driver Licenses"])
service = DriverLicenseService()

@router.get("/me")
@log_execution
def get_user_driver_license(db: DB, current_user: User = Depends(get_current_user)):
    return service.get_user_driver_license(db, current_user.user_id)