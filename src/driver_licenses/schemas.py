from pydantic import BaseModel
from enum import Enum

class LicenseType(Enum):
    M = "M"
    A = "A"
    A1 = "A1"
    B = "B"
    B1 = "B1"
    BE = "BE"
    C1 = "C1"
    D1 = "D1"

class DriverLicenseBase(BaseModel):
    license_number: str
    license_type: LicenseType
    expiry_date: str

class DriverLicenseResponse(DriverLicenseBase):
    model_config = {"from_attributes": True}
    
    driver_license_id: int