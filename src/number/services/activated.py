from fastapi import Depends, HTTPException

from src.number.repository.number import NumberRepository
from src.number.repository.rest import RestRepository
from src.number.schemas.models import Activated, Rest
from src.number.schemas.number import AddServiceSchema
from src.service.repository.addition import AdditionRepository
from src.service.repository.addition_category import CategoryRepository
from src.service.repository.common_service import ServiceRepository
from src.service.repository.tarif import TarifRepository
from src.service.shemas.models import Tarif, Addition
from src.transaction.services.write_off import WriteOffService
from src.transaction.repository.write_off import WrifeOffRepository

class NumberService:
    def __init__(self, service_repository: ServiceRepository = Depends(ServiceRepository),
                 number_repository: NumberRepository = Depends(NumberRepository),
                 tarif_repository: TarifRepository = Depends(TarifRepository),
                 addition_repository: AdditionRepository = Depends(AdditionRepository),
                 rest_repository: RestRepository = Depends(RestRepository),
                 category_repository: CategoryRepository = Depends(CategoryRepository),
                 write_off_repository: WrifeOffRepository = Depends(WrifeOffRepository)):
        self.service_repository = service_repository
        self.number_repository = number_repository
        self.tarif_repository = tarif_repository
        self.addition_repository = addition_repository
        self.rest_repository = rest_repository
        self.category_repository = category_repository
        self.write_off_repository = write_off_repository

    def get_services(self, ids: list[int]):
        for id in ids:
            if self.service_repository.existed_id(id) is None:
                raise HTTPException(status_code=500,
                                    detail=f"Service with {id} doen't exist")

