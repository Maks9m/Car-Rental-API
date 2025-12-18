from fastapi import APIRouter
from typing import List
from src.database import DB
from src.models import Payment
from src.payments.schemas import PaymentResponse

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/", response_model=List[PaymentResponse])
def get_all_payments(db: DB):
    return db.query(Payment).all()