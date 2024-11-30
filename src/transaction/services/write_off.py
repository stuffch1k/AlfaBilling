from datetime import timedelta

from src.number.repository.number import NumberRepository
from src.transaction.repository.write_off import WrifeOffRepository
from fastapi import Depends, HTTPException

from src.transaction.schemas.models import WriteOff
from src.transaction.schemas.write_off import DateFilterSchema, ReadSchema
from src.service.services.common_service import get_service_name


class WriteOffService:
    def __init__(self, number_repository: NumberRepository = Depends(NumberRepository),
                 write_off_repository: WrifeOffRepository = Depends(WrifeOffRepository)):
        self.number_repository = number_repository
        self.write_off_repository = write_off_repository

    def create_write_off(self, _number_id: int, _activated_id: int, price: float):
        self.number_repository.decrease_balance(_number_id, price)
        write_off = WriteOff(amount = price, activated_id = _activated_id,
                             number_id = _number_id)
        self.write_off_repository.create_write_off(write_off)

    def get_write_off(self, body: DateFilterSchema) -> list[ReadSchema]:
        if self.number_repository.get_number_by_id(body.number_id) is None:
            raise HTTPException(status_code=500,
                                detail=f"Number with pk {body.number_id} doesn't exist")
        body.date_end += timedelta(seconds=20)
        write_off = self.write_off_repository.get_write_off(body)
        # service_id = self.number_repository.get_service_by_activated(write_off.activated_id)
        # _service_name = get_service_name(service_id)
        result = []
        for e in write_off:
            result.append(ReadSchema(price=e.amount, date=e.date, activated_id=e.activated_id))
        return result

