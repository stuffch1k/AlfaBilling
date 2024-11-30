from src.number.repository.number import NumberRepository
from src.transaction.repository.payment import PaymentRepository
from fastapi import Depends, HTTPException
from datetime import timedelta
from src.transaction.schemas.models import Payment
from src.transaction.schemas.payment import CreateSchema, DateFilterSchema, ReadSchema


class PaymentService:
    def __init__(self, number_repository: NumberRepository = Depends(NumberRepository),
                 payment_repository: PaymentRepository = Depends(PaymentRepository)):
        self.number_repository = number_repository
        self.payment_repository = payment_repository

    def create_payment(self, body: CreateSchema):
        if self.number_repository.get_number_by_id(body.number_id) is None:
            raise HTTPException(status_code=500,
                                detail=f"Number with pk {body.number_id} doesn't exist")
        self.payment_repository.create_payment(Payment(**body.__dict__))
        self.number_repository.increase_balance(body.number_id, body.amount)

    def get_payments(self, body: DateFilterSchema) -> list[ReadSchema]:
        if self.number_repository.get_number_by_id(body.number_id) is None:
            raise HTTPException(status_code=500,
                                detail=f"Number with pk {body.number_id} doesn't exist")
        body.date_end+=timedelta(seconds=20)
        payments = self.payment_repository.get_payments(body)
        result = []
        for payment in payments:
            result.append(ReadSchema(amount=payment.amount, date=payment.date))
        return result

