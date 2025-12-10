from fastapi import APIRouter, Depends
from src.api.users.service import get_all_users
from src.api import dependencies
from sqlalchemy.orm import Session



router = APIRouter()
    
    
@router.get("/")
async def read_users(db: Session = Depends(dependencies.get_db)):
    return get_all_users(db)