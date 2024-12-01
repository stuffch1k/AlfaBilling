from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..schemas.models import Activated
from ...database import database


class ActivatedRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def get_service_id(self, _id: int):
        return self.session.query(Activated).filter_by(id=_id).first().service_id

    def get_today_service(self, date_start, date_end):
        return self.session.\
            query(Activated.id, Activated.service_id, Activated.number_id). \
            filter(and_(Activated.expiration_date >= date_start,
                        Activated.expiration_date <= date_end)).all()

    def update_date(self, _id: int, _activation_date, _expiration_date):
        self.session.query(Activated).filter_by(id = _id).\
            update({'activation_date':_activation_date, 'expiration_date':_expiration_date})
        self.session.commit()
        self.session.flush()