from fastapi import Depends, HTTPException
from starlette import status

from src.number.schemas.models import PhoneNumber
from src.number.services.number import NumberService

from src.auth.schemas.client import ClientSchema
from src.user.schemas.client import ClientFullSchema, ClientInfoSchema, ClientShortSchema
from src.auth.schemas.operator import OperatorSchema
from src.auth.services.auth import AuthService
from src.user.repository.user import UserRepository


class UserService:
    def __init__(self, number_service: NumberService = Depends(NumberService),
                 auth_service: AuthService = Depends(AuthService),
                 user_repository: UserRepository = Depends(UserRepository)):
        self.number_service = number_service
        self.auth_service = auth_service
        self.user_repository = user_repository

    def add_number_to_client(self, client_id, number_str):
        client = self.auth_service.get_client_by_id(client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Client with id {client_id} doesn't exist")
        number = self.auth_service.create_number_from_str(number_str)
        if number in client.numbers:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Client {client_id} already has number {number_str}")
        return self.user_repository.add_number(client, number)

    def get_all_client_numbers(self, client_id: int) -> list[str]:
        all_numbers = []
        client = self.auth_service.get_client_by_id(client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Client with id {client_id} doesn't exist")
        for number in client.numbers:
            all_numbers.append(number.phone_number)
        return all_numbers

    def get_main(self, user: OperatorSchema | ClientSchema) -> ClientFullSchema | OperatorSchema:
        if isinstance(user, OperatorSchema):
            return user
        # client: Client = self.auth_service.get_client_by_id(user.id)
        return self.get_client_main_by_number(user.login_number)

    def get_client_main_by_number(self, number_str: str):
        number_info = self.number_service.get_number_info(number_str)
        client_info = self.get_client_info(number_str)
        return ClientFullSchema(number_info=number_info, client_info=client_info)

    def get_client_info(self, number_str: str):
        client = self.auth_service.get_client_by_number(number_str)
        client_schema = ClientInfoSchema.model_validate(client)
        client_schema.number = number_str
        return client_schema

    def get_all_clients(self, page: int, size: int) -> list[ClientShortSchema]:
        result = []
        numbers: list[PhoneNumber] = self.number_service.get_all_numbers(page, size)
        for number in numbers:
            client_schema = self.create_short_client_schema(number)
            result.append(client_schema)
        return result

    def create_short_client_schema(self, number: PhoneNumber) -> ClientShortSchema:
        phone_number: str = number.phone_number
        balance: float = number.balance
        tarif = self.number_service.get_activated_tarif(number.id)
        if tarif:
            _tarif_name = tarif.name
        else:
            _tarif_name = None
        client = self.auth_service.get_client_by_id(number.client_id)
        client_schema = ClientShortSchema.model_validate(client)
        client_schema.number = phone_number
        client_schema.balance = balance
        client_schema.tarif_name = _tarif_name
        return client_schema
