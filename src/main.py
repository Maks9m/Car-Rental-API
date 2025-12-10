from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.api import dependencies
from src.config import config
from src.api import main_router


app = FastAPI(title=config.PROJECT_NAME)

app.include_router(main_router)
