from fastapi import FastAPI
from src.users import users_router
from src.config import config

app = FastAPI(title=config.APP_NAME)

# Include routers
app.include_router(users_router, prefix="/users", tags=["Users"])