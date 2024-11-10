from fastapi import APIRouter, Depends

from src.auth.permissions import permissions
from src.service.services.common_service import Service
from src.service.shemas.tarif import *
from src.service.services.tarif import *

tarif_router = APIRouter(tags=["Tarif"])

@tarif_router.post('/')
def create_tarif(tarif: CreateSchema,
                 service: TarifService = Depends(),
                 user = Depends(permissions.allowAll)):
    service.create_tarif(tarif)

@tarif_router.get('/', response_model=list[ShortReadSchema])
def get_tarif_list(service: TarifService = Depends(),
                   user = Depends(permissions.allowAll)):
    return service.get_tarif_list()

@tarif_router.get('/{id}', response_model=FullReadSchema)
def get_tarif_by_name(id: int, service: TarifService = Depends(),
                      user = Depends(permissions.allowAll)):
    return service.get_tarif_by_id(id)

@tarif_router.patch('/{id}')
def update_tarif(id: int, tarif: UpdateSchema,
                 service: TarifService = Depends(),
                 user = Depends(permissions.allowAll)):
    return service.update_tarif(id, tarif)

