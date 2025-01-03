from fastapi import Depends
from sqlalchemy.orm import Session

from ..shemas.models import AdditionCategory
from ...database import database

class CategoryRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def create_category(self, category: AdditionCategory):
        '''
        Доавбление категории Услуги
        '''
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)

    def get_category_by_id(self, id: int):
        '''
        Select по id
        '''
        return self.session.query(AdditionCategory).filter(AdditionCategory.id == id).first()


    def get_category_by_name(self, name: str):
        '''
        Select по name
        '''
        return self.session.query(AdditionCategory).filter(AdditionCategory.name == name).first()

    def get_category_list(self):
        '''
        select *
        '''
        return self.session.query(AdditionCategory).all()
