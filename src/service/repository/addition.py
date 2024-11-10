from fastapi import Depends
from sqlalchemy.orm import Session

from ..shemas.models import Addition
from ...database import database


class AdditionRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session
        
    def create_addition(self, addition: Addition):
        '''
        Добавление записи Доп услуги
        '''
        self.session.add(addition)
        self.session.commit()
        self.session.refresh(addition)

    def get_addition_by_id(self, id: int):
        '''
        Select по ID Доп услуги
        '''
        return self.session.query(Addition).filter(Addition.service_id == id).first()

    def get_addition_list(self):
        '''
        select *
        '''
        return self.session.query(Addition).all()

    def update_addition(self, id: int, addition):
        self.session.query(Addition).filter(Addition.service_id == id).update(addition)
        self.session.commit()
        self.session.flush()
    def get_addition(self, id: int):
        return self.session.query(Addition).filter(Addition.service_id == id).first()

    def get_categorial_list_by_id(self, id: int):
        return self.session.query(Addition).filter(Addition.category_id == id).all()
