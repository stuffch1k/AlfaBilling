from fastapi import Depends, HTTPException

from src.service.repository.common_service import ServiceRepository
from src.service.repository.tarif import TarifRepository
from src.service.shemas.models import Tarif
from src.service.shemas.tarif import *


class TarifService:
    def __init__(self, service_repository: ServiceRepository = Depends(ServiceRepository),
                 tarif_repository: TarifRepository = Depends(TarifRepository)):
        self.service_repository = service_repository
        self.tarif_repository = tarif_repository


    def create_tarif(self, tarif: CreateSchema) -> None:
        '''
        Создание тарифа - служебный роут.
        После деплоя снести
        '''
        parsed_tarif: Tarif = Tarif(**tarif.dict())
        # name is unique, поэтому кидаем 500
        if self.is_existed_name(parsed_tarif.name):
            raise HTTPException(status_code=500,
                                detail=f"Tarif with name {parsed_tarif.name} already exists")
        # берем pk aka fk от родиетльской сущности Service
        pk = self.service_repository.create_service_key()
        tarif = Tarif(
            service_id=pk,
            name=parsed_tarif.name,
            description=parsed_tarif.description,
            price=parsed_tarif.price,
            duration=parsed_tarif.duration,
            internet=parsed_tarif.internet,
            is_unlimited_internet=parsed_tarif.is_unlimited_internet,
            minute=parsed_tarif.minute,
            sms=parsed_tarif.sms
        )
        self.tarif_repository.create_tarif(tarif)

    def get_tarif_list(self) -> list[ShortReadSchema]:
        '''
        Возвращает перечень тарифов.
        На морде планируется отображение карточек с выжимкой информации
        Args:
            смотри ShortReadSchema
        '''
        tarif_list = self.tarif_repository.get_tarif_list()
        return tarif_list

    def get_tarif_by_name(self, name: str) -> FullReadSchema:
        '''
        Подробная информации о тарифе в карточке
        Args:
            FullReadSchema
        '''
        # name is unique, поэтому кидаем 500
        if not self.is_existed_name(name):
            raise HTTPException(status_code=500,
                                detail=f"Probably invalid option 'name':"
                                       f"tarif with name {name} don't exist")
        tarif = self.tarif_repository.get_tarif_by_name(name)
        return tarif

    def is_existed_name(self, name: str) -> bool:
        '''
        Хэлпер, проверяем существует ли тариф с таким именем
        '''
        tarif = self.tarif_repository.get_tarif_by_name(name)
        if tarif:
            return True
        else:
            return False
