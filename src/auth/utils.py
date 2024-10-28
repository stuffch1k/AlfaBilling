from passlib.context import CryptContext

from .schemas.client import ClientSchema
from .schemas.operator import OperatorSchema
from .schemas.models import Operator, Client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_operator_data(operator: Operator) -> OperatorSchema:
    return OperatorSchema.model_validate(operator)


def create_client_data(client: Client, number: str) -> ClientSchema:
    client_data = ClientSchema.model_validate(client)
    client_data.login_number = number
    return client_data
