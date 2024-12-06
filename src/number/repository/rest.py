from fastapi import Depends
from sqlalchemy.orm import Session

from ..schemas.models import PhoneNumber, Activated, Rest
from ..schemas.rest import AddRestSchema
from ...database import database
from itertools import islice

class RestRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def add_or_update(self, rest: Rest):
        '''
        Создание или обновление сущности
        Не нашла в алхимии спец средства, поэтому так
        '''
        rests_ = self.session.query(Rest).filter(Rest.number_id == rest.number_id).first()
        if rests_ is None:
            self.session.add(rest)
            self.session.commit()
            self.session.refresh(rest)
        else:
            # итерация нужно во избежание пары ошибок
            # AttributeError: "sqlalchemy" object has no attribute "items" but it doesn't
            # Лишнее поле при анпаке - срезать проще
            self.session.query(Rest).filter(Rest.number_id == rest.number_id).update(dict(islice(rest.__dict__.items(), 1, None)))
            self.session.commit()
            self.session.flush()

    def get_rests(self, number_id: int):
        return self.session.query(Rest).filter(Rest.number_id == number_id).first()

    def get_all_rows(self):
        return self.session.query(Rest).all()

    def decrease_internet(self, _num_id: int, amount: int):
        self.session.query(Rest).filter_by(number_id=_num_id).update({"internet": amount})
        self.session.commit()
        self.session.flush()

    def decrease_minute(self, _num_id: int, amount: int):
        self.session.query(Rest).filter_by(number_id=_num_id).update({"minute": amount})
        self.session.commit()
        self.session.flush()

    def decrease_sms(self, _num_id: int, amount: int):
        self.session.query(Rest).filter_by(number_id=_num_id).update({"sms": amount})
        self.session.commit()
        self.session.flush()

    def decrease_all(self, _id: int, internet: int, minute: int, sms: int):
        self.session.query(Rest).filter_by(id=_id).\
            update({"internet": internet, "minute": minute, "sms": sms})
        self.session.commit()
        self.session.flush()

