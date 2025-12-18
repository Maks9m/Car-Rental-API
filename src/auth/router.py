from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.database import DB

from src.auth.service import AuthService
from src.auth.schema import TokenResponse

router = APIRouter(tags=["Authentication"])
auth_service = AuthService()

@router.post("/token", response_model=TokenResponse)
def login_for_access_token(db: DB, form_data: OAuth2PasswordRequestForm = Depends()):
    return auth_service.authenticate_user(db, form_data.username, form_data.password)