from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class PaymentResponse(BaseModel):
    payment_id: int
    trip_id: int
    amount: Decimal
    status: str
    payment_date: datetime

    model_config = {"from_attributes": True}