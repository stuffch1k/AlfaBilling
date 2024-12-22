from fastapi import Depends, HTTPException

from src.service.repository.addition import AdditionRepository
from src.service.repository.addition_category import CategoryRepository
from src.service.shemas.category import *
from src.service.shemas.models import AdditionCategory


class CategoryService:
    def __init__(self, category_repository: CategoryRepository = Depends(CategoryRepository),
                 addition_repository: AdditionRepository = Depends(AdditionRepository)):
        self.category_repository = category_repository
        self.addition_repository = addition_repository

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

    def get_category_list(self) -> list[FullReadSchema]:
        '''
        Возвращает перечень категорий.
        Args:
            смотри ReadSchema
        '''
        category_list = self.category_repository.get_category_list()
        result = []
        for category in category_list:
            _count = len(self.addition_repository.get_categorial_list_by_id(category.id))
            ans = FullReadSchema(id=category.id,
                                 name=category.name,
                                 count=_count,
                                 ru_name=TYPES[category.name])
            result.append(ans)
        return result

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