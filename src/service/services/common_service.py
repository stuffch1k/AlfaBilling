from src.service.repository.addition import AdditionRepository
from src.service.repository.tarif import TarifRepository
from src.service.services.tarif import TarifService


def get_service_name(service_id: int):
    tarif_repository = TarifRepository()
    tarif = tarif_repository.get_tarif_by_id(service_id)
    if tarif:
        return tarif.name
    addition_repository = AdditionRepository()
    return addition_repository.get_addition_by_id(service_id).name
