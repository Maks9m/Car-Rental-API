from sqlalchemy.orm import Session
from src.models import User

def get_all_users(db: Session):
    # Placeholder function to simulate fetching all users from the database
    return db.query(User).all()
    