from fastapi import APIRouter, Depends
from src.database import DB
from src.users import service
from src.users.schemas import UserResponse
from src.users.dependencies import valid_user_id
from src.models import User


router = APIRouter()


@router.get("", response_model=list[UserResponse])
def get_all_users(db: DB):
    return service.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user: User = Depends(valid_user_id)):
    return user
