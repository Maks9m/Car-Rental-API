from pydantic import validate_email
from src.database import DB
from src.users import service
from src.users.exceptions import UserNotFound
from src.models import User


def valid_user_id(user_id: int, db: DB) -> User:
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise UserNotFound(user_id)
    return user