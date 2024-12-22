from fastapi import APIRouter, Depends

from src.auth.permissions import permissions
from src.service.services.addition_category import CategoryService
from src.service.shemas.category import CreateSchema, ReadSchema, FullReadSchema

category_router = APIRouter(tags=["Addition Category"])


@category_router.post('/')
def create_category(category: CreateSchema,
                 service: CategoryService = Depends(),
                 user = Depends(permissions.allowAll)):
    service.create_category(category)

@category_router.get('/', response_model=list[FullReadSchema])
def get_category_list(service: CategoryService = Depends(),
                   user = Depends(permissions.allowAll)):
    category_list = service.get_category_list()
    return category_list

@category_router.get('/{id}', response_model=ReadSchema)
def get_category(id:int, service: CategoryService = Depends(),
                      user = Depends(permissions.allowAll)):
    category = service.get_category(id)
    return category