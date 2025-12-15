from pydantic import BaseModel, Field
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
    license_number: str = Field(..., min_length=5, max_length=20, description="Unique driver license number")

class DriverLicenseResponse(DriverLicenseBase):
    model_config = {"from_attributes": True}
    
    driver_license_id: int

class DriverLicenseCreate(DriverLicenseBase):
    license_type: LicenseType
    expiry_date: str = Field(..., description="Expiry date in ISO format (YYYY-MM-DD)")
