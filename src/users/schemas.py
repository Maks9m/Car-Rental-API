from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field

from src.driver_licenses.schemas import DriverLicenseCreate


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class UserRegister(UserBase):
    password: str = Field(..., min_length=8)
    driver_license: DriverLicenseCreate

class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    driver_license_id: int | None = None


class UserResponse(UserBase):
    model_config = {"from_attributes": True}
    
    user_id: int

class UserRankingResponse(BaseModel):
    user_id: int
    firstname: str
    lastname: str
    total_bookings: int
    total_spent: Decimal
    rank: int

class UserCreate(UserBase):
    password_hash: str
    driver_license_id: int

class UserInfo(UserBase):
    model_config = {"from_attributes": True}

    user_id: int
    password_hash: str
    driver_license_id: int
