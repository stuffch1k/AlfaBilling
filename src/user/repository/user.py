from fastapi import Depends
from sqlalchemy.orm import Session

from src.number.schemas.models import PhoneNumber
from ...database import database
from src.auth.schemas.models import Client


class UserRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def add_number(self, client: Client, number: PhoneNumber):
        client.numbers.append(number)
        self.session.add(client)
        self.session.commit()
