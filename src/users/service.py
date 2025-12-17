from sqlalchemy.orm import Session

from src.models import User
from src.logger import log_execution

from src.auth.utils import hash_password

from src.driver_licenses.repository import DriverLicenseRepository
from src.driver_licenses.exceptions import DriverLicenseAlreadyExists

from src.users.schemas import UserCreate, UserInfo, UserResponse, UserRegister, UserUpdate
from src.users.exceptions import UserNotFound, EmptyUsersTable, UserAlreadyExists
from src.users.repository import UserRepository


class UserService:
    def __init__ (self):
        self.user_repo = UserRepository()
        self.license_repo = DriverLicenseRepository()

    @log_execution
    def get_all(self, db: Session) -> list[User]:
        all_users = self.user_repo.get_all(db)
        if not all_users:
            raise EmptyUsersTable()
        return all_users

    @log_execution
    def get_user_by_id(self, db: Session, user_id: int) -> UserResponse:
        user = self.user_repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFound(user_id)
        return user

    @log_execution
    def get_user_by_email(self, db: Session, email: str) -> UserResponse:
        user = self.user_repo.get_by_email(db, email)
        if not user:
            raise UserNotFound()
        return user
    
    @log_execution
    def get_user_info(self, db: Session, email: str) -> UserInfo:
        user = self.user_repo.get_by_email(db, email)
        if not user:
            raise UserNotFound()
        return user
    
    @log_execution
    def register(self, db: Session, user_data: UserRegister) -> UserResponse:
        if self.user_repo.get_by_email(db, user_data.email):
            raise UserAlreadyExists(user_data.email)
        
        if self.license_repo.get_by_number(db, user_data.driver_license.license_number):
            raise DriverLicenseAlreadyExists(user_data.driver_license.license_number)
        
        try:
            
            new_license = self.license_repo.create(db, user_data.driver_license)

            user_create_data = UserCreate(
                 email=user_data.email,
                 firstname=user_data.firstname,
                 lastname=user_data.lastname,
                 password_hash=hash_password(user_data.password),
                 driver_license_id=new_license.driver_license_id
            )

            new_user = self.user_repo.create(db, user_create_data)

            db.commit()
            db.refresh(new_user)
            return new_user
        
        except Exception as e:
            db.rollback()
            raise e
        
    @log_execution
    def update_user_info(self, db: Session, user_id: int, update_data: UserUpdate) -> UserResponse:
        user = self.user_repo.get_by_id(db, user_id)    
        if not user:
            raise UserNotFound(user_id)
        
        updated_user = self.user_repo.update(db, user, update_data)
        return updated_user