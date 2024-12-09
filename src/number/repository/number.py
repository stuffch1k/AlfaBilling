from fastapi import Depends
from sqlalchemy.orm import Session

from ..schemas.models import PhoneNumber, Activated
from ...database import database

class NumberRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def existed_number(self, number: str):
        return self.session.query(PhoneNumber).\
            filter(PhoneNumber.phone_number == number).first()

    def get_number_id(self, number: str) -> int:
        return self.session.query(PhoneNumber).\
            filter(PhoneNumber.phone_number == number).first().id

    def add_service(self, activated: Activated) -> int:
        self.session.add(activated)
        self.session.commit()
        self.session.refresh(activated)
        return activated.id

    def activated_list(self) -> list[int]:
        return self.session.query(Activated.service_id).all()

    def decrease_balance(self, number_id: int, price: float):
        balance = self.get_balance(number_id)
        self.session.query(PhoneNumber).\
            filter(PhoneNumber.id == number_id).update({'balance': balance - price})
        self.session.commit()

    def increase_balance(self, number_id: int, amount: float):
        balance = self.get_balance(number_id)
        self.session.query(PhoneNumber). \
            filter(PhoneNumber.id == number_id).update({'balance': balance + amount})
        self.session.commit()

    def get_balance(self, number_id: int):
        return self.session.query(PhoneNumber).filter(PhoneNumber.id == number_id).first().balance

    def get_service_by_activated(self, activated_id: int):
        return self.session.query(Activated).filter_by(id=activated_id).service_id

    def get_number_by_id(self, number_id: int):
        return self.session.query(PhoneNumber).filter_by(id=number_id).first()

    def deactivate_service(self, activated: Activated):
        activated.expiration_date = None
        self.session.add(activated)
        self.session.commit()

    def get_all_numbers(self, page, size):
        offset_value = (page - 1) * size
        query = (self.session.query(PhoneNumber).order_by(PhoneNumber.client_id.desc()).limit(size).offset(offset_value))
        return query.all()

    def get_activated_by_id(self, activated_id) -> Activated | None:
        return self.session.query(Activated).get(activated_id)

    def get_activated_by_id_and_number(self, activated_id, number_id) -> Activated | None:
        return self.session.query(Activated).filter(Activated.id == activated_id
                                                    and Activated.number_id == number_id).first()

    def get_all_activated(self, number_id) -> list[Activated]:
        return self.session.query(Activated).filter(Activated.number_id == number_id).all()

    def get_number_by_str_representation(self, number: str):
        return self.session.query(PhoneNumber).filter(PhoneNumber.phone_number == number).first()

