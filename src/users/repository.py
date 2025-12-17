from sqlalchemy.orm import Session

from src.models import User
from src.logger import log_execution

from src.users.schemas import UserCreate

class UserRepository:
    def get_all(self, db: Session) -> list[User]:
        return db.query(User).all()
    
    def get_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.user_id == user_id).first()
    
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()
    
    @log_execution
    def create(self, db: Session, user_data: UserCreate) -> User:
        new_user = User(
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            email=user_data.email,
            password_hash=user_data.password_hash,
            driver_license_id=user_data.driver_license_id,
        )
        db.add(new_user)
        db.flush()
        return new_user
    
    @log_execution
    def update(self, db: Session, user: User, update_data: UserCreate) -> User:
        if update_data.firstname:
            user.firstname = update_data.firstname
        if update_data.lastname:
            user.lastname = update_data.lastname
        if update_data.email:
            user.email = update_data.email
        if update_data.driver_license_id:
            user.driver_license_id = update_data.driver_license_id

        db.commit()
        db.refresh(user)
        return user
