from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.database import get_db
from src.logger import log_execution
from src.auth.service import AuthService
from src.auth.schema import TokenResponse

router = APIRouter(tags=["Authentication"])
auth_service = AuthService()

@router.post("/token", response_model=TokenResponse)
@log_execution
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_service.authenticate_user(db, form_data.username, form_data.password)