from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ...database import database
from src.transaction.schemas.models import WriteOff, Payment


class PaymentRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def create_payment(self, _payment: Payment):
        self.session.add(_payment)
        self.session.commit()
        self.session.refresh(_payment)

    def get_payments(self, body):
        return self.session.query(Payment).\
            filter(and_(Payment.number_id == body.number_id,
                        Payment.date >= body.date_start,
                        Payment.date <= body.date_end)).all()
