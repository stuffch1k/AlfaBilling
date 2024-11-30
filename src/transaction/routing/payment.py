from fastapi import APIRouter, Depends

from src.auth.permissions import permissions
from src.transaction.schemas.payment import CreateSchema, DateFilterSchema, ReadSchema
from src.transaction.services.payment import PaymentService

payment_router = APIRouter(tags=["Payment"])

@payment_router.post("")
def create_payment(body: CreateSchema,
                   service: PaymentService = Depends()):
    return service.create_payment(body)

@payment_router.post("/history", response_model=list[ReadSchema])
def get_payment_history(body: DateFilterSchema,
                        service: PaymentService = Depends()):
    return service.get_payments(body)