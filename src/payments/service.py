from src.payments.repository import PaymentRepository
from src.models import Payment

class PaymentService:
    def __init__(self):
        self.repo = PaymentRepository()

    def get_history(self, db):
        return db.query(Payment).all() 