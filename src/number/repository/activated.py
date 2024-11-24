from fastapi import Depends
from sqlalchemy.orm import Session

from ..schemas.models import Activated
from ...database import database

class ActivatedRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def get_service_id(self, _id: int):
        return self.session.query(Activated).filter_by(id=_id).first().service_id
