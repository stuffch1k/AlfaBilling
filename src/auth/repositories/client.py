from fastapi import Depends
from sqlalchemy.orm import Session
from ...database import database
from ...models import Client, PhoneNumber


class ClientRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

    def find_number(self, number: str) -> PhoneNumber:
        number: PhoneNumber = self.session.query(PhoneNumber).filter(PhoneNumber.Phone_number == number).first()
        return number

    def find_passport(self, passport: str) -> Client:
        client: Client = self.session.query(Client).filter(Client.Passport == passport).first()
        return client

    def find_contract(self, contract_number: str) -> Client:
        client: Client = self.session.query(Client).filter(Client.Contract_number == contract_number).first()
        return client

    def find_client_by_number(self, number: PhoneNumber) -> Client:
        client: Client = self.session.query(Client).filter(Client.Id == number.Client_id).first()
        return client

    def get_client_by_id(self, client_id: int) -> Client:
        client: Client = self.session.query(Client).get(client_id)
        return client

    def add_client_to_db(self, client: Client) -> None:
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
