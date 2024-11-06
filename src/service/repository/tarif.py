from fastapi import Depends
from sqlalchemy.orm import Session

from ..shemas.models import Tarif
from ...database import database


class TarifRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def create_tarif(self, tarif: Tarif):
        '''
        Добавление записи тарифа
        '''
        self.session.add(tarif)
        self.session.commit()
        self.session.refresh(tarif)

    def get_tarif_by_name(self, name: str):
        '''
        Select по названию тарифа
        '''
        return self.session.query(Tarif).filter(Tarif.name == name).first()

    def get_tarif_list(self):
        '''
        select *
        '''
        return self.session.query(Tarif).all()
