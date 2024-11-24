from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ...database import database
from src.transaction.schemas.models import WriteOff

class WrifeOffRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def create_write_off(self, write_off: WriteOff):
        self.session.add(write_off)
        self.session.commit()
        self.session.refresh(write_off)

    def get_write_off(self, body):
        return self.session.query(WriteOff).\
            filter(and_(WriteOff.number_id == body.number_id,
                        WriteOff.date >= body.date_start,
                        WriteOff.date <= body.date_end)).all()
