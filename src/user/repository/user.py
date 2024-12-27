from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_

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

    def get_clients_by_fio_substring(self, surname: str, name: str, patronymic: str):
        name = "%{}%".format(name)
        surname = "%{}%".format(surname)
        patronymic = "%{}%".format(patronymic)
        return self.session.query(Client).filter(and_(Client.name.like(name),
                                                      Client.surname.like(surname),
                                                      Client.patronymic.like(patronymic))).all()

