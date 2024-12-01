from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
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

    def get_today_service(self):
        # test day
        day = datetime(year=2024, month=12, day=15, hour=12, minute=33)
        # real day
        # day = datetime.today()
        date_start = day - timedelta(minutes=10)
        date_end = day + timedelta(minutes=10)
        return self.activated_repository.get_today_service(date_start, date_end)

    def update_activated(self, services: list[tuple], duration: dict):
        for service in services:
            activation_date = datetime.today()
            expiration_date = activation_date+timedelta(days=duration[service[1]])
            self.activated_repository.update_date(service[0], activation_date, expiration_date)




