from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.api import dependencies
from src.config import config


app = FastAPI(title=config.PROJECT_NAME)

@app.get("/test")
def test_check(db: Session = Depends(dependencies.get_db)):
    return {"status": "ok"}
