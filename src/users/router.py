from fastapi import APIRouter, Depends, status

from src.logger import log_execution
from src.models import User
from src.database import DB

from src.auth.dependencies import get_current_user

from src.users.service import UserService
from src.users.schemas import UserResponse, UserRegister, UserInfo, UserUpdate


router = APIRouter(prefix="/users", tags=["Users"])
service = UserService()


@router.get("", response_model=list[UserResponse])
@log_execution
def get_all_users(db: DB):
    return service.get_all(db)

@router.get("/me", response_model=UserInfo)
@log_execution
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
@log_execution
def get_user_by_id(user_id: int, db: DB):
    return service.get_user_by_id(db, user_id)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@log_execution
def register_user(user_data: UserRegister, db: DB):
    return service.register(db, user_data)

@router.patch("/me/update", response_model=UserUpdate)
@log_execution
def update_current_user_info(update_data: UserUpdate, db: DB, current_user: User = Depends(get_current_user)):
    return service.update_user_info(db, current_user.user_id, update_data)