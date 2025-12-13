from sqlalchemy.orm import Session
from src.models import User
from src.users.schemas import UserBase, UserResponse
from src.users.exceptions import UserNotFound

def get_all_users(db: Session) -> list[UserResponse]:
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int) -> UserResponse | None:
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise UserNotFound(user_id)
    return user

def get_user_by_email(db: Session, email: str) -> UserResponse | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise UserNotFound()
    return user