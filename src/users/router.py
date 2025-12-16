from fastapi import APIRouter, Depends, status
from src.models import User
from src.database import DB
from src.users.service import UserService
from src.users.schemas import UserResponse, UserRegister, UserInfo
from src.auth.dependencies import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])
service = UserService()


@router.get("", response_model=list[UserResponse])
def get_all_users(db: DB):
    return service.get_all(db)

@router.get("/me", response_model=UserInfo)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: DB):
    return service.get_user_by_id(db, user_id)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db: DB):
    return service.register(db, user_data)