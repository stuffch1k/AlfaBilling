from fastapi import Depends, HTTPException

from src.number.repository.number import NumberRepository
from src.number.schemas.models import Activated
from src.number.schemas.number import AddServiceSchema
from src.service.repository.common_service import ServiceRepository
from src.service.repository.tarif import TarifRepository


class NumberService:
    def __init__(self, service_repository: ServiceRepository = Depends(ServiceRepository),
                 number_repository: NumberRepository = Depends(NumberRepository),
                 tarif_repository: TarifRepository = Depends(TarifRepository)):
        self.service_repository = service_repository
        self.number_repository = number_repository
        self.tarif_repository = tarif_repository

    def add_service(self, body: AddServiceSchema):
        if not self.existed_id(body.service_id):
            raise HTTPException(status_code=500,
                                detail=f"Service with pk {body.service_id} doesn't exist")
        if not self.existed_number(body.phone_number):
            raise HTTPException(status_code=500,
                                detail=f"Number {body.phone_number} doesn't exist")
        if self.is_tarif(body.service_id) and self.already_has_tarif(body.service_id):
            raise HTTPException(status_code=500,
                                detail=f"Number {body.phone_number} already has active tarif."
                                       f"Wanna change it?")
        number_id = self.get_number_id(body.phone_number)
        self.number_repository.add_service(
            Activated(service_id=body.service_id, number_id=number_id))

    def existed_id(self, service_id: int):
        id = self.service_repository.existed_id(service_id)
        if id is not None:
            return True
        else:
            return False

    def existed_number(self, number: str):
        number = self.number_repository.existed_number(number)
        if number is not None:
            return True
        else:
            return False

    def get_number_id(self, number: str) -> int:
        return self.number_repository.get_number_id(number)

    def is_tarif(self, service_id: int) -> bool:
        tarif = self.tarif_repository.get_tarif_by_id(service_id)
        return True if tarif is not None else False

    def already_has_tarif(self, service_id: int) -> bool:
        '''
        Check if client already has activated tarif
        Предполгаю
        Не может быть подключено несоклько тарифов на номере
        '''
        tarif_list = set(self.tarif_repository.get_tarifs_id())
        activated_ = set(self.number_repository.activated_list())
        tarif_id = tarif_list & activated_
        return True if tarif_id is not None else False

