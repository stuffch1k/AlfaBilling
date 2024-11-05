from fastapi import APIRouter, Depends

from src.auth.permissions import permissions
from src.service.services.addition import AdditionService
from src.service.services.common_service import Service
from src.service.shemas.addition import *
from src.service.shemas.category import ChooseSchema

addition_router = APIRouter(tags=["Addition"])

@addition_router.post('/')
def create_addition(addition: CreateSchema,
                    service: AdditionService = Depends(),
                    user = Depends(permissions.allowAll)):
    service.create_addition(addition)

@addition_router.get('/', response_model=list[ShortReadSchema])
def get_addition_list(service: AdditionService = Depends(),
                      user = Depends(permissions.allowAll)):
    return service.get_addition_list()

@addition_router.get('/category', response_model=list[ShortReadSchema])
def get_categorial_additions(category_id: int,
                             service: AdditionService = Depends(),
                             user = Depends(permissions.allowAll)):
    return service.get_categorial_list(category_id)

@addition_router.get('/{addition_id}', response_model=FullReadSchema)
def get_addition(addition_id: int,
                service: AdditionService = Depends(),
                user = Depends(permissions.allowAll)):
    return service.get_addition(addition_id)



