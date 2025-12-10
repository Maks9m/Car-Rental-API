from src.api.users import router as users_router
from fastapi import APIRouter

main_router = APIRouter()

main_router.include_router(users_router, prefix="/users")
