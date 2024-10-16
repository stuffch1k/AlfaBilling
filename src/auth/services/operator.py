from fastapi import HTTPException, Depends
from starlette import status

from ..schemas.operator import OperatorCreateSchema, OperatorSchema, OperatorLoginSchema
from ..repositories.operator import OperatorRepository
from ..utils import hash_password, verify_password
from src.auth.schemas.models import Operator


class AuthOperatorService:
    def __init__(self, repository: OperatorRepository = Depends(OperatorRepository)):
        self.repository = repository

    def register_operator(self, operator_data: OperatorCreateSchema) -> OperatorSchema:
        if self.get_existing_operator_by_email(operator_data.Email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Аккаунт с таким email уже существует')
        new_operator: Operator = self.create_operator_from_schema(operator_data)
        self.repository.add_operator_to_db(new_operator)
        return OperatorSchema.model_validate(new_operator)

    def authenticate_operator(self, operator_data: OperatorLoginSchema) -> Operator:
        operator: Operator = self.get_existing_operator_by_email(operator_data.Email)
        if not operator:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Аккаунта с таким email не существует')
        if not verify_password(operator_data.Password, operator.Hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Неверный пароль')
        return operator

    def get_existing_operator_by_email(self, email: str) -> Operator | None:
        return self.repository.find_operator_by_email(email)

    def get_operator_by_id(self, operator_id: int) -> Operator:
        return self.repository.get_operator_by_id(operator_id)

    @classmethod
    def create_operator_from_schema(cls, operator_data: OperatorCreateSchema) -> Operator:
        operator = Operator(
            Name=operator_data.Name,
            Surname=operator_data.Surname,
            Email=operator_data.Email,
            Hashed_password=hash_password(operator_data.Password)
        )
        return operator
