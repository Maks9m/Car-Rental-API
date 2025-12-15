from sqlalchemy.orm import Session
from src.models import User

from src.users.schemas import UserResponse, UserRegister
from src.users.exceptions import UserNotFound, EmptyUsersTable, UserAlreadyExists
from src.users.repository import UserRepository

from src.auth.utils import hash_password

from src.driver_licenses.repository import DriverLicenseRepository
from driver_licenses.exceptions import DriverLicenseAlreadyExists


class UserService:
    def __init__ (self):
        self.user_repo = UserRepository()
        self.license_repo = DriverLicenseRepository()

    def get_all(self, db: Session) -> list[User]:
        all_users = self.user_repo.get_all(db)
        if not all_users:
            raise EmptyUsersTable()
        return all_users

    def get_user_by_id(self, db: Session, user_id: int) -> UserResponse | None:
        user = self.user_repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFound(user_id)
        return user

    def get_user_by_email(self, db: Session, email: str) -> UserResponse | None:
        user = self.user_repo.get_by_email(db, email)
        if not user:
            raise UserNotFound()
        return user
    
    def register(self, db: Session, user_data: UserRegister) -> UserResponse:
        if self.user_repo.get_by_email(db, user_data.email):
            raise UserAlreadyExists(user_data.email)
        
        if self.license_repo.get_by_number(db, user_data.license_number):
            raise DriverLicenseAlreadyExists(user_data.license_number)
        
        try:
            license_data = {
                "license_number": user_data.license_number,
                "license_type": user_data.license_type,
                "expiry_date": user_data.expiry_date
            }

            new_license = self.license_repo.create(db, license_data)

            user_create_data = {
                "firstname": user_data.firstname,
                "lastname": user_data.lastname,
                "email": user_data.email,
                "password_hash": hash_password(user_data.password),
                "driver_license_id": new_license.driver_license_id
            }

            new_user = self.user_repo.create(db, user_create_data)

            db.commit()
            db.refresh(new_user)
            return new_user
        
        except Exception as e:
            db.rollback()
            raise e
        