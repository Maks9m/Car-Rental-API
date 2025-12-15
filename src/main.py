from fastapi import FastAPI
from src.users import router as users_router
from src.auth import router as auth_router
from src.config import config

app = FastAPI(title=config.APP_NAME)

# Include routers
app.include_router(users_router)
app.include_router(auth_router)
