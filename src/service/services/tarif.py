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
        if self.is_existed_name(tarif.name):
            raise HTTPException(status_code=500,
                                detail=f"Tarif with name {tarif.name} already exists")
        # берем pk aka fk от родиетльской сущности Service
        pk = self.service_repository.create_service_key()
        tarif = Tarif(service_id=pk, **tarif.dict())
        self.tarif_repository.create_tarif(tarif)

    def get_tarif_list(self) -> list[TarifReadSchema]:
        '''
        Возвращает перечень тарифов.
        На морде планируется отображение карточек с выжимкой информации
        Args:
            смотри ShortReadSchema
        '''
        return self.tarif_repository.get_tarif_list()

    def get_tarif_by_id(self, id: int) -> FullReadSchema:
        if not self.is_existed_id(id):
            raise HTTPException(status_code=500,
                                detail="Incorrect option ID")
        return self.tarif_repository.get_tarif_by_id(id)

    def update_tarif(self, id: int, tarif: UpdateSchema) -> None:
        if not self.is_existed_id(id):
            raise HTTPException(status_code=500,
                                detail="Incorrect option ID")
        tarif_old = self.tarif_repository.get_tarif_by_id(id)
        # tarif_old.internet = tarif.internet
        # tarif_old.is_unlimited_internet = tarif.is_unlimited_internet
        # tarif_old.minute = tarif.minute
        # tarif_old.sms = tarif.sms
        return self.tarif_repository.update_tarif(id, tarif.__dict__)

    def is_existed_name(self, name: str) -> bool:
        '''
        Хэлпер, проверяем существует ли тариф с таким именем
        '''
        tarif = self.tarif_repository.get_tarif_by_name(name)
        if tarif:
            return True
        else:
            return False

    def is_existed_id(self, id: int) -> bool:
        tarif = self.tarif_repository.get_tarif_by_id(id)
        if tarif:
            return True
        else:
            return False
