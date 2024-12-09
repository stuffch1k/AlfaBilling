from fastapi import APIRouter, Depends, Query

from src.auth.permissions import permissions
from src.service.services.addition import AdditionService
from src.service.shemas.addition import *
from src.service.shemas.category import ChooseSchema

addition_router = APIRouter(tags=["Addition"])

@addition_router.post('/')
def create_addition(addition: CreateSchema,
                    service: AdditionService = Depends(),
                    user=Depends(permissions.allowOperator)):
    service.create_addition(addition)

@addition_router.get('/', response_model=list[ShortReadSchema])
def get_addition_list(service: AdditionService = Depends(),
                      page: int = Query(1, ge=1),
                      size: int = Query(10, ge=1, le=50)):
    return service.get_addition_list(page, size)

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

@addition_router.patch('/{id}')
def update_addition(addition_id: int,
                    addition_data: UpdateSchema,
                    service: AdditionService = Depends(),
                    user=Depends(permissions.allowAll)):
    return service.update_addition(addition_id, addition_data)


