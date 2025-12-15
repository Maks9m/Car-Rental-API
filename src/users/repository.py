from sqlalchemy.orm import Session
from src.models import User
from src.users.schemas import UserCreate

class UserRepository:
    def get_all(self, db: Session) -> list[User]:
        return db.query(User).all()
    
    def get_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.user_id == user_id).first()
    
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()
    
    def create(self, db: Session, user_data: UserCreate) -> User:
        new_user = User(
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            email=user_data.email,
            password_hash=user_data.password,
            license_number=user_data.license_number,
            license_type=user_data.license_type,
            expiry_date=user_data.expiry_date
        )
        db.add(new_user)
        db.flush()
        return new_user
    

    



