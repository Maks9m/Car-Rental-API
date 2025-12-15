from fastapi import Depends, Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from src.database import get_db
from src.models import User
from src.config import config
from src.exceptions import Unauthorized
from src.users.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    try:
        
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_email: str = payload.get("sub")

        if user_email is None:
            raise Unauthorized("Could not validate credentials")
        
    except JWTError:
        raise Unauthorized("Could not validate credentials")
    
    user_repo = UserRepository()
    user = user_repo.get_by_email(db, user_email)

    if user is None:
        raise Unauthorized("Could not validate credentials")
    
    return user
