from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.core import settings


app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/health")
def health_check(db: Session = Depends(deps.get_db)):
    return {"status": "ok"}
