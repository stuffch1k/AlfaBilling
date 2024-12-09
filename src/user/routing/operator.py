from fastapi import APIRouter, Depends, Query

from src.user.services.user import UserService

operator_router = APIRouter(tags=["Operator"])


@operator_router.get("/clients")
def get_all_clients(user_service: UserService = Depends(),
                    page: int = Query(1, ge=1),
                    size: int = Query(10, ge=1, le=50)):
    """
    Список всех клиентов (пока без фильтрации)
    """
    return user_service.get_all_clients(page, size)


@operator_router.get("/client")
def get_client_by_number(number: str,
                         user_service: UserService = Depends()):
    """Инфа о клиенте по номеру телефона"""
    return user_service.get_client_main_by_number(number)