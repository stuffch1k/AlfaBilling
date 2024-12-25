from fastapi import APIRouter, Depends

from src.auth.permissions import permissions
from src.transaction.schemas.payment import CreateSchema, DateFilterSchema, ReadSchema
from src.transaction.services.payment import PaymentService
from src.transaction.services.write_off import WriteOffService

transaction_router = APIRouter(tags=["Transaction"])


@transaction_router.post("/history")
def get_transaction_history(body: DateFilterSchema,
                            payment_service: PaymentService = Depends(),
                            write_off_service: WriteOffService = Depends()):
    payments = payment_service.get_payments(body)
    write_offs = write_off_service.get_write_off(body)
    result = []
    result.extend(payments)
    result.extend(write_offs)
    return sorted(result, key=lambda d: d.date)