import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_NAME: str = "Car Rental API"
    
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

config = Config()