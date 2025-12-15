from fastapi import APIRouter, Depends
from src.database import DB
from src.users.service import UserService
from src.users.schemas import UserResponse, UserRegister


router = APIRouter()
service = UserService()


@router.get("", response_model=list[UserResponse])
def get_all_users(db: DB):
    return service.get_all(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: DB):
    return service.get_user_by_id(db, user_id)

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserRegister, db: DB):
    return service.register(db, user_data)