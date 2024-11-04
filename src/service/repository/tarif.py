from fastapi import Depends
from sqlalchemy.orm import Session

from ..shemas.models import Tarif
from ...database import database


class TarifRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def create_tarif(self, tarif: Tarif):
        self.session.add(tarif)
        self.session.commit()
        self.session.refresh(tarif)

    def get_tarif_by_name(self, name: str):
        tarif = self.session.query(Tarif).filter(Tarif.name == name).first()
        return tarif

    def get_tarif_list(self):
        tarif_list = self.session.query(Tarif).all()
        return tarif_list
