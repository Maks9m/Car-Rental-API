from fastapi import APIRouter, Depends
from src.database import DB
from src.users import service
from src.users.schemas import UserResponse, UserCreate
from src.users.dependencies import valid_email, valid_user_id
from src.models import User


router = APIRouter()


@router.get("", response_model=list[UserResponse])
def get_all_users(db: DB):
    result =service.get_all_users(db)
    return result


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: DB):
    user = service.get_user_by_id(db, user_id)
    return user

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: DB):
    ...