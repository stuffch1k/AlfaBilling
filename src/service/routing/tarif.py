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
    tarif_list = service.get_tarif_list()
    return tarif_list
