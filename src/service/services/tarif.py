from fastapi import Depends, HTTPException

from src.service.repository.common_service import ServiceRepository
from src.service.repository.tarif import TarifRepository
from src.service.shemas.models import Tarif
from src.service.shemas.tarif import CreateSchema


class TarifService:
    def __init__(self, service_repository: ServiceRepository = Depends(ServiceRepository),
                 tarif_repository: TarifRepository = Depends(TarifRepository)):
        self.service_repository = service_repository
        self.tarif_repository = tarif_repository


    def create_tarif(self, tarif: CreateSchema) -> None:
        parsed_tarif: Tarif = Tarif(**tarif.dict())
        if self.is_existed(parsed_tarif.name):
            raise HTTPException(status_code=500,
                                detail=f"Tarif with name {parsed_tarif.name} already exists")
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

    def is_existed(self, name: str) -> bool:
        tarif = self.tarif_repository.get_tarif_by_name(name)
        if tarif:
            return True
        else:
            return False
