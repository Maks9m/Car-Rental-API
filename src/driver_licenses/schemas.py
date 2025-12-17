from pydantic import BaseModel, Field
from datetime import date
from src.models import LicenseType as ModelLicenseType


class DriverLicenseBase(BaseModel):
    license_number: str = Field(..., min_length=5, max_length=20, description="Unique driver license number")

class DriverLicenseResponse(DriverLicenseBase):
    model_config = {"from_attributes": True}
    
    driver_license_id: int

class DriverLicenseCreate(DriverLicenseBase):
    license_type: ModelLicenseType
    expiry_date: date = Field(..., description="Expiry date in ISO format (YYYY-MM-DD)")
