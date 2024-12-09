from fastapi import APIRouter, Depends

from src.number.schemas.number import AddNumberSchema
from src.auth.services.user import get_current_user
from src.auth.schemas.client import ClientSchema
from src.auth.schemas.operator import OperatorSchema
from src.user.services.user import UserService
from src.user.schemas.client import ClientFullSchema

main_router = APIRouter(tags=["Main"])
client_router = APIRouter(tags=["Client"])


@main_router.get("/", response_model= ClientFullSchema | OperatorSchema)
def main(user: OperatorSchema | ClientSchema = Depends(get_current_user),
         user_service: UserService = Depends()):
    """
    Инфа по залогиненному юзеру (номер телефона, остатки и т.д.)
    """
    return user_service.get_main(user)


@client_router.post("/{client_id}/number")
def add_number_to_client(client_id: int,
                         number: AddNumberSchema,
                         user_service: UserService = Depends()):
    """
    Добавление номера телефона к клиенту
    """
    return user_service.add_number_to_client(client_id, number.phone_number)


@client_router.get("/{client_id}/numbers")
def get_all_client_numbers(client_id: int,
                           user_service: UserService = Depends()):
    """Список номеров клиента"""
    return user_service.get_all_client_numbers(client_id)


