from fastapi import APIRouter, Depends

from src.auth.permissions import permissions
from src.transaction.schemas.write_off import DateFilterSchema, ReadSchema
from src.transaction.services.write_off import WriteOffService

write_off_router = APIRouter(tags=["WriteOff"])

@write_off_router.post("", response_model=list[ReadSchema])
def get_write_off(body: DateFilterSchema, service: WriteOffService = Depends(),
                  user = Depends(permissions.allowAll)):
    """
    Сюда нужн пермишн.
    Оператор получает любые списания.
    Юзер только свои.
    """
    return service.get_write_off(body)

@write_off_router.post("/script")
def emulate_write_off():
    pass
