from fastapi import Depends

from src.service.repository.addition import AdditionRepository
from src.service.repository.common_service import ServiceRepository
from src.service.repository.tarif import TarifRepository
from src.service.services.tarif import TarifService


def get_service_name(service_id: int):
    tarif_repository = TarifRepository()
    tarif = tarif_repository.get_tarif_by_id(service_id)
    if tarif:
        return tarif.name
    addition_repository = AdditionRepository()
    return addition_repository.get_addition_by_id(service_id).name

class CommonService:
    def __init__(self, service_repository: ServiceRepository = Depends(ServiceRepository),
                 tarif_repository: TarifRepository = Depends(TarifRepository),
                 addition_repository: AdditionRepository = Depends(AdditionRepository)):
        self.service_repository = service_repository
        self.addition_repository = addition_repository
        self.tarif_repository = tarif_repository
    def get_service_price(self, ids:list[int]):
        result = {}
        for service_id in ids:
            tarif_price = self.tarif_repository.get_tarif_price(service_id)
            if tarif_price:
                result[service_id] = tarif_price[0]
            else:
                result[service_id] = self.addition_repository.get_addition_price(service_id)
        return result

    def get_service_duration(self, ids: list[int]):
        result = {}
        for service_id in ids:
            tarif_duration = self.tarif_repository.get_tarif_duration(service_id)
            if tarif_duration:
                result[service_id] = tarif_duration[0]
            else:
                result[service_id] = self.addition_repository.get_addition_duration(service_id)
        return result

