from typing import List, Type

from fastapi import Depends
from sqlalchemy.orm import Session

from ..shemas.models import Tarif
from ...database import database


class TarifRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def create_tarif(self, tarif: Tarif) -> None:
        '''
        Добавление записи тарифа
        '''
        self.session.add(tarif)
        self.session.commit()
        self.session.refresh(tarif)


    def get_tarif_list(self) -> list[Type[Tarif]]:
        '''
        select *
        '''
        return self.session.query(Tarif).all()

    def update_tarif(self, id: int, tarif):
        self.session.query(Tarif).filter(Tarif.service_id == id).update(tarif)
        self.session.commit()
        self.session.flush()

    def get_tarif_by_id(self, id: int) -> Tarif:
        return self.session.query(Tarif).filter(Tarif.service_id == id).first()

    def get_tarif_by_name(self, name: str) -> Tarif:
        '''
        Select по названию тарифа
        '''
        return self.session.query(Tarif).filter(Tarif.name == name).first()

    def get_tarifs_id(self) -> list[int]:
        return self.session.query(Tarif.service_id).all()

    def get_tarif_price(self, tarif_id: int) -> tuple[float]:
        return self.session.query(Tarif.price).filter(Tarif.service_id == tarif_id).first()

    def get_tarif_duration(self, tarif_id: int) -> tuple[int]:
        return self.session.query(Tarif.duration).filter(Tarif.service_id == tarif_id).first()

