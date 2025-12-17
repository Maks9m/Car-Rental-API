from sqlalchemy import func, select, desc
from sqlalchemy.orm import Session

from src.models import User, Booking, Trip, Payment, Status
from src.logger import log_execution

from src.users.schemas import UserCreate

class UserRepository:
    def get_all(self, db: Session) -> list[User]:
        return db.query(User).all()
    
    def get_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.user_id == user_id).first()
    
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()
    
    def get_ranking(self, db: Session) -> list[User]:
        """
        Повертає рейтинг користувачів за кількістю бронювань та витратами.
        """
        query = (
            select(
                User.user_id,
                User.firstname,
                User.lastname,
                func.count(Booking.book_id).label("total_bookings"),
                func.sum(Payment.amount).label("total_spent"),
                func.dense_rank().over(
                    order_by=[
                        func.count(Booking.book_id).desc(),
                        func.sum(Payment.amount).desc()
                    ]
                ).label("rank")
            )
            .join(Booking, User.user_id == Booking.user_id)
            .join(Trip, Booking.book_id == Trip.book_id)
            .join(Payment, Trip.trip_id == Payment.trip_id)
            .where(Booking.status != Status.CANCELED)
            .group_by(User.user_id, User.firstname, User.lastname)
            .order_by("rank")
        )
        
        result = db.execute(query).all()
        return result
    
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
