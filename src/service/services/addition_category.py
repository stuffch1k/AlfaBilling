from fastapi import Depends, HTTPException

from src.service.repository.addition_category import CategoryRepository
from src.service.shemas.category import *
from src.service.shemas.models import AdditionCategory


class CategoryService:
    def __init__(self, category_repository: CategoryRepository = Depends(CategoryRepository)):
        self.category_repository = category_repository

    def create_category(self, category: CreateSchema) -> None:
        '''
        Создание тарифа - служебный роут.
        После деплоя снести
        '''
        parsed_category: AdditionCategory = AdditionCategory(**category.dict())
        # name is unique, поэтому кидаем 500
        if self.is_existed_name(parsed_category.name):
            raise HTTPException(status_code=500,
                                detail=f"Category with name {parsed_category.name} already exists")

        self.category_repository.create_category(parsed_category)

    def get_category_list(self) -> list[ReadSchema]:
        '''
        Возвращает перечень категорий.
        Args:
            смотри ReadSchema
        '''
        category_list = self.category_repository.get_category_list()
        return category_list

    def get_category(self, id: int) -> ReadSchema:
        '''
        Фильтр категорий
        Args:
            ReadSchema
        '''
        if not self.is_existed_id(id):
            raise HTTPException(status_code=500,
                                detail=f"Probably invalid option 'id':"
                                       f"category with id {id} don't exist")
        category = self.category_repository.get_category_by_id(id)
        return category

    def is_existed_id(self, id: int) -> bool:
        '''
        Хэлпер, проверяем существует ли тариф с таким id
        '''
        category = self.category_repository.get_category_by_id(id)
        if category:
            return True
        else:
            return False

    def is_existed_name(self, name: str) -> bool:
        '''
                Хэлпер, проверяем существует ли тариф с таким name
                '''
        category = self.category_repository.get_category_by_name(name)
        if category:
            return True
        else:
            return False