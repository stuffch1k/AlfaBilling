from fastapi import Depends
from sqlalchemy.orm import Session

from ..schemas.models import PhoneNumber, Activated
from ...database import database

class NumberRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def existed_number(self, number: str):
        return self.session.query(PhoneNumber).filter(PhoneNumber.phone_number == number).first()

    def get_number_id(self, number: str) -> int:
        return self.session.query(PhoneNumber).filter(PhoneNumber.phone_number == number).first().id

    def add_service(self, activated: Activated):
        self.session.add(activated)
        self.session.commit()
        self.session.refresh(activated)

    def activated_list(self) -> list[int]:
        return self.session.query(Activated.service_id).all()
