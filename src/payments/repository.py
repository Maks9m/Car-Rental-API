from sqlalchemy.orm import Session
from src.models import Payment, Status, PaymentType
from datetime import datetime
from decimal import Decimal

class PaymentRepository:
    def create_pending_payment(self, db: Session, trip_id: int, amount: Decimal):
        """Створює запис про платіж у статусі PENDING."""
        new_payment = Payment(
            trip_id=trip_id,
            amount=amount,
            payment_date=datetime.now(),
            payment_type=PaymentType.CREDIT_CARD,
            status=Status.PENDING
        )
        db.add(new_payment)
        return new_payment