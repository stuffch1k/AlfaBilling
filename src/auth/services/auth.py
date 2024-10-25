from fastapi import Depends, HTTPException
from starlette import status

from ..repositories.operator import OperatorRepository
from ..repositories.client import ClientRepository
from ..schemas.models import Operator, Client, PhoneNumber
from ..schemas.operator import OperatorCreateSchema, OperatorSchema, OperatorLoginSchema
from ..schemas.client import ClientSchema, ClientCreateSchema, ClientLoginSchema
from ..utils import hash_password, verify_password


class AuthService:
    """
        Используется для регистрации и аутентификации операторов и клиентов
    """

    def __init__(self, operator_repository: OperatorRepository = Depends(OperatorRepository),
                 client_repository: ClientRepository = Depends(ClientRepository)):
        self.client_repository = client_repository
        self.operator_repository = operator_repository

    def register_user(self, user_data: OperatorCreateSchema | ClientCreateSchema) -> OperatorSchema | ClientSchema:
        """
        Регистрирует пользователя
        :param user_data: pydantic модель клиента или оператора для регистрации
        :return: pydantic модель зарегистрированного клиента или оператора
        """
        if isinstance(user_data, OperatorCreateSchema):
            return self.register_operator(user_data)
        return self.register_client(user_data)

    def register_operator(self, operator_data: OperatorCreateSchema) -> OperatorSchema | HTTPException:
        """
        Создает новую модель оператора и добавляет ее в бд
        :param operator_data: pydantic модель оператора при регистрации
        :return: pydantic модель созданного оператора или HTTPException,
        если оператор с указанным email уже существует в бд
        """
        if self.get_existing_operator_by_email(operator_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Аккаунт с таким email уже существует')
        new_operator: Operator = self.create_operator_from_schema(operator_data)
        self.operator_repository.add_operator_to_db(new_operator)
        return OperatorSchema.model_validate(new_operator)

    def register_client(self, client_data: ClientCreateSchema) -> ClientSchema | HTTPException:
        """
        Создает новую модель клиента и добавляет ее в бд
        :param client_data: pydantic модель клиента при регистрации
        :return: pydantic модель созданного клиента или HTTPException,
        если клиент с указанным номером, паспортом или номером договора уже существует в бд
        """
        if self.client_repository.find_number(client_data.number):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Клиент с таким номером уже существует')
        if self.client_repository.find_passport(client_data.passport):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Клиент с таким паспортом уже существует')
        if self.client_repository.find_contract(client_data.contract_number):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Клиент с таким номером договора уже существует')

        new_client: Client = self.create_client_from_schema(client_data)
        self.client_repository.add_client_to_db(new_client)
        return ClientSchema.model_validate(new_client)

    def authenticate_user(self, user_data: OperatorLoginSchema | ClientLoginSchema) -> Operator | Client:
        """
        Аутентифицирует пользователя
        :param user_data: pydantic модель клиента или оператора для аутентификации
        :return: аутентифицированная модель клиента или оператора
        """
        if isinstance(user_data, OperatorLoginSchema):
            return self.authenticate_operator(user_data)
        return self.authenticate_client(user_data)

    def authenticate_operator(self, operator_data: OperatorLoginSchema) -> Operator:
        """
        Проверяет соответсвие указанных почты и пароля с теми, которые лежат в бд
        :param operator_data: pydantic модель оператора для аутентификации
        :return: модель оператора из бд или HTTPException,
        если почта или пароль указаны неверно
        """
        operator: Operator = self.get_existing_operator_by_email(operator_data.email)
        if not operator or not verify_password(operator_data.password, operator.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Неверный email или пароль')
        return operator

    def authenticate_client(self, client_data: ClientLoginSchema) -> Client:
        """
        Проверяет соответсвие указанных номера и пароля с теми, которые лежат в бд
        :param client_data: pydantic модель клиента для аутентификации
        :return: модель клиента из бд или HTTPException,
        если номер или пароль указаны неверно
        """
        self.check_number(client_data.number)
        client: Client = self.get_client_by_number(client_data.number)
        if not verify_password(client_data.password, client.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Неверный пароль')
        return client

    def get_existing_operator_by_email(self, email: str) -> Operator | None:
        """
        Возвращает модель оператора из бд по почте
        :param email: почта оператора
        :return: модель оператора или None, если оператора с указанной почтой не найден
        """
        return self.operator_repository.find_operator_by_email(email)

    def check_number(self, number: str) -> None:
        """
        Проверяет, существует ли указанный номер в бд
        :param number: номер
        :return: HTTPException, если номера не существует
        """
        if not self.client_repository.find_number(number):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Клиента с таким номером не существует")

    def get_existing_number(self, number: str) -> PhoneNumber | None:
        """
        Возвращает модель номера телефона из бд по его строковому значению
        :param number: номер телефона
        :return: модель номера телефона или None, если номер не найден
        """
        return self.client_repository.find_number(number)

    def get_client_by_number(self, number: str) -> Client | None:
        """
        Возвращает модель клиента из бд по строковому значению номера телефона
        :param number: номер телефона
        :return: модель клиента из бд или None, если клиент с таким номером телефона не найден
        """
        phone_number: PhoneNumber = self.get_existing_number(number)
        return self.client_repository.find_client_by_number(phone_number)

    def get_client_by_id(self, client_id: int) -> Client | None:
        """
        Возвращает модель клиента из бд по id
        :param client_id: id клиента
        :return: модель клиента или None, если клиент с указанным id не найден
        """
        return self.client_repository.get_client_by_id(client_id)

    def get_operator_by_id(self, operator_id: int) -> Operator | None:
        """
        Возвращает модель оператора из бд по id
        :param operator_id: id оператора
        :return: модель оператора или None, если оператор с указанным id не найден
        """
        return self.operator_repository.get_operator_by_id(operator_id)

    @classmethod
    def create_operator_from_schema(cls, operator_data: OperatorCreateSchema) -> Operator:
        """
        Создает модель оператора из pydantic модели
        :param operator_data: pydantic модель оператора для регистрации
        :return: модель оператора
        """
        operator = Operator(
            name=operator_data.name,
            surname=operator_data.surname,
            email=operator_data.email,
            hashed_password=hash_password(operator_data.password)
        )
        return operator

    @classmethod
    def create_client_from_schema(cls, client_data: ClientCreateSchema) -> Client:
        """
        Создает модель клиента из pydantic модели
        :param client_data: pydantic модель клиента для регистрации
        :return: модель клиента
        """
        number: PhoneNumber = cls.create_number_from_str(client_data.number)
        client = Client(
            name=client_data.name,
            surname=client_data.surname,
            patronymic=client_data.patronymic,
            contract_number=client_data.contract_number,
            passport=client_data.passport,
            hashed_password=hash_password(client_data.password)
        )
        client.numbers.append(number)
        return client

    @classmethod
    def create_number_from_str(cls, number: str) -> PhoneNumber:
        """
        Создает модель номера телефона из его строкового значения
        :param number: номер телефона
        :return: модель номера телефона
        """
        number = PhoneNumber(
            phone_number=number
        )
        return number
