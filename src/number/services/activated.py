from fastapi import Depends, HTTPException

from src.number.repository.activated import ActivatedRepository
from src.number.repository.number import NumberRepository
from src.service.repository.common_service import ServiceRepository

class ActivatedService:
    def __init__(self, service_repository: ServiceRepository = Depends(ServiceRepository),
                 activated_repository: ActivatedRepository = Depends(ActivatedRepository),
                 number_repository: NumberRepository = Depends(NumberRepository)):
        self.service_repository = service_repository
        self.activated_repository = activated_repository
        self.number_repository = number_repository

    def get_services(self, ids: list[int]) -> list[int]:
        service_ids = []
        for id in ids:
            service_id = self.activated_repository.get_service_id(id)
            if service_id is None:
                raise HTTPException(status_code=500,
                                    detail=f"Activated with {id} doen't exist")
            service_ids.append(service_id)
        return service_ids

