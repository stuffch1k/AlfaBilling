from fastapi import Depends, HTTPException
from starlette import status

from ..repositories.client import ClientRepository
from ..schemas.client import ClientCreateSchema, ClientSchema, ClientLoginSchema
from ...models import Client, PhoneNumber
from ..utils import verify_password, hash_password


class AuthClientService:
    def __init__(self, repository: ClientRepository = Depends(ClientRepository)):
        self.repository = repository

    def register_client(self, client_data: ClientCreateSchema) -> ClientSchema:
        if self.repository.find_number(client_data.Number):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Клиент с таким номером уже существует')
        if self.repository.find_passport(client_data.Passport):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Клиент с таким паспортом уже существует')
        if self.repository.find_contract(client_data.Contract_number):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Клиент с таким номером договора уже существует')

        new_client: Client = self.create_client_from_schema(client_data)
        self.repository.add_client_to_db(new_client)
        return ClientSchema.model_validate(new_client)

    def authenticate_client(self, client_data: ClientLoginSchema) -> Client:
        self.check_number(client_data.Number)
        client: Client = self.get_client_by_number(client_data.Number)
        if not verify_password(client_data.Password, client.Hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Неверный пароль')
        return client

    def check_number(self, number: str) -> None:
        if not self.repository.find_number(number):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Клиента с таким номером не существует")

    def get_existing_number(self, number: str) -> PhoneNumber:
        return self.repository.find_number(number)

    def get_client_by_number(self, number: str) -> Client:
        phone_number: PhoneNumber = self.get_existing_number(number)
        return self.repository.find_client_by_number(phone_number)

    def get_client_by_id(self, client_id: int) -> Client:
        return self.repository.get_client_by_id(client_id)

    @classmethod
    def create_client_from_schema(cls, client_data: ClientCreateSchema) -> Client:
        number: PhoneNumber = cls.create_number_from_str(client_data.Number)
        client = Client(
            Name=client_data.Name,
            Surname=client_data.Surname,
            Patronymic=client_data.Patronymic,
            Contract_number=client_data.Contract_number,
            Passport=client_data.Passport,
            Hashed_password=hash_password(client_data.Password)
        )
        client.Numbers.append(number)
        return client

    @classmethod
    def create_number_from_str(cls, number: str) -> PhoneNumber:
        number = PhoneNumber(
            Phone_number=number
        )
        return number


