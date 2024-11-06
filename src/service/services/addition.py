from fastapi import Depends, HTTPException

from src.service.repository.addition import AdditionRepository
from src.service.repository.addition_category import CategoryRepository
from src.service.repository.common_service import ServiceRepository
from src.service.shemas.addition import *
from src.service.shemas.models import Addition


class AdditionService:
    def __init__(self, service_repository: ServiceRepository = Depends(ServiceRepository),
                 addition_repository: AdditionRepository = Depends(AdditionRepository),
                 category_repository: CategoryRepository = Depends(CategoryRepository)):
        self.service_repository = service_repository
        self.addition_repository = addition_repository
        self.category_repository = category_repository

    def create_addition(self, addition: CreateSchema) -> None:
        if not self.category_repository.get_category_by_id(addition.category_id):
            raise HTTPException(status_code=500,
                                detail=f"Category with pk {addition.category_id} doesn't exist")
        # берем pk aka fk от родиетльской сущности Service
        pk = self.service_repository.create_service_key()
        addition = Addition(service_id=pk, **addition.dict())
        self.addition_repository.create_addition(addition)

    def get_addition_list(self) -> list[ShortReadSchema]:
        return self.addition_repository.get_addition_list()

    def get_categorial_list(self, category_id: int):
        if not self.category_repository.get_category_by_id(category_id):
            raise HTTPException(status_code=500,
                                detail=f"Category with pk {category_id} doesn't exist")
        return self.addition_repository.get_categorial_list_by_id(category_id)

    def get_addition(self, id: int) -> FullReadSchema:
        return self.addition_repository.get_addition(id)

    def is_existed_name(self, name: str) -> bool:
        addition = self.addition_repository.get_addition_by_name(name)
        if addition:
            return True
        else:
            return False
