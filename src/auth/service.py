from datetime import timedelta
from sqlalchemy.orm import Session

from src.config import config
from src.logger import log_execution

from src.auth.exceptions import UnauthorizedAction
from src.auth.utils import create_access_token, verify_password
from src.auth.schema import TokenResponse

from src.users.repository import UserRepository

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    @log_execution
    def authenticate_user(self, db: Session, email: str, password: str) -> TokenResponse:

        user = self.user_repo.get_by_email(db, email)

        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedAction()

        access_token_expires = config.ACCESS_TOKEN_EXPIRE_MINUTES
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.user_id},
            expires_delta=timedelta(minutes=access_token_expires)
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
