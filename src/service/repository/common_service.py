from fastapi import Depends
from sqlalchemy.orm import Session

from ..shemas.models import Service
from ...database import database

class ServiceRepository:
    def __init__(self, session: Session = Depends(database.get_session)) -> None:
        self.session = session

    def create_service_key(self) -> int:
        '''
        Создание сущности-родителя Service.
        Возвращает свой PK для записи тарифов и услуг
        '''
        service_key = Service()
        self.session.add(service_key)
        self.session.flush()
        self.session.refresh(service_key)
        return service_key.id

    def existed_id(self, id: int):
        '''
        Проверяем есть ли услга с данным id
        '''
        return self.session.query(Service).filter(Service.id == id).first()
