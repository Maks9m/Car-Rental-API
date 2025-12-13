from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class UserCreate(UserBase):
    driver_license_id: int | None = None
    password: str

class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    driver_license_id: int | None = None


class UserResponse(UserBase):
    model_config = {"from_attributes": True}
    
    user_id: int
    driver_license_id: int | None
