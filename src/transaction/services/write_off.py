from datetime import timedelta

from src.number.repository.number import NumberRepository
from src.transaction.repository.write_off import WrifeOffRepository
from fastapi import Depends, HTTPException

from src.transaction.schemas.models import WriteOff
from src.transaction.schemas.write_off import DateFilterSchema, ReadSchema, FullReadSchema
from src.service.services.common_service import CommonService
from src.service.repository.addition import AdditionRepository
from src.service.repository.common_service import ServiceRepository
from src.service.repository.tarif import TarifRepository


class WriteOffService:
    def __init__(self, number_repository: NumberRepository = Depends(NumberRepository),
                 write_off_repository: WrifeOffRepository = Depends(WrifeOffRepository),
                 service_repository: ServiceRepository = Depends(ServiceRepository),
                 tarif_repository: TarifRepository = Depends(TarifRepository),
                 addition_repository: AdditionRepository = Depends(AdditionRepository)
                 ):
        self.number_repository = number_repository
        self.write_off_repository = write_off_repository
        self.service_repository = service_repository
        self.addition_repository = addition_repository
        self.tarif_repository = tarif_repository

    def create_write_off(self, _number_id: int, _activated_id: int, price: float):
        self.number_repository.decrease_balance(_number_id, price)
        write_off = WriteOff(amount = price, activated_id = _activated_id,
                             number_id = _number_id)
        self.write_off_repository.create_write_off(write_off)

    def get_write_off(self, body: DateFilterSchema) -> list[FullReadSchema]:
        if self.number_repository.get_number_by_id(body.number_id) is None:
            raise HTTPException(status_code=500,
                                detail=f"Number with pk {body.number_id} doesn't exist")
        body.date_end += timedelta(seconds=20)
        write_off = self.write_off_repository.get_write_off(body)

        result = []
        common_service = CommonService(self.service_repository, self.tarif_repository, self.addition_repository)
        for e in write_off:
            service_id = self.number_repository.get_service_by_activated(e.activated_id)
            _service_name = common_service.get_service_name(service_id)
            _service_amount = common_service.get_service_amount(service_id)
            result.append(FullReadSchema(name=_service_name, price=e.amount,
                                         date=e.date, amount=_service_amount))
        return result

    def create_write_off_list(self, services: list[tuple], prices: dict):
        for service in services:
            _price = prices[service[1]]
            _number_id = service[2]
            self.number_repository.decrease_balance(_number_id, _price)
            write_off = WriteOff(amount=_price, activated_id=service[0],
                                 number_id=_number_id)
            self.write_off_repository.create_write_off(write_off)


