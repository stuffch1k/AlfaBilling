from fastapi import APIRouter, Depends

from src.auth.permissions import permissions
from src.number.schemas.number import AddServiceSchema, DeactivateServiceSchema
from src.number.services.activated import ActivatedService
from src.number.services.number import NumberService

'''
idk насколько нужно разделять эти роуты,
но у остатков будет как минимум еще один эндпоинт
'''

activated_router = APIRouter(tags=["Activated service"])
number_router = APIRouter(tags=["Number"])


@activated_router.post("/")
def add_service(schema: AddServiceSchema,
                service: NumberService = Depends(),
                user=Depends(permissions.allowAll)):
    return service.add_service(schema)


@activated_router.delete("/")
def deactivate_service(schema: DeactivateServiceSchema,
                       service: NumberService = Depends(),
                       user=Depends(permissions.allowAll)):
    """
    Отключение услуги у номера
    """
    return service.deactivate_service(schema)


@activated_router.get("/{activated_id}")
def get_activated_service(activated_id: int,
                          service: NumberService = Depends(),
                          user=Depends(permissions.allowAll)):
    """
    Инфа о подключенном тарифе или услуге по id
    """
    return service.get_activated_service_by_id(activated_id)


@activated_router.post("/services")
def get_service_id(ids: list[int],
                   service: ActivatedService = Depends()):
    """
    Получить service_id (те, которые в справочнике услуг) по подключенным к номеру.
    Это для списаний, наверное
    """
    return service.get_services(ids)

@number_router.get("/rest")
def get_rests(number: str,
                service: NumberService = Depends(),
                user = Depends(permissions.allowAll)):
    return service.get_rests(number)


@number_router.get("/{number_id}/activated")
def get_activated_list(number_id: int,
                       service: NumberService = Depends()):
    """
    Инфа о подключенном тарифе и список всех подключенных услуг на номере
    """
    activated_tarif, activated_additions = service.get_activated_services(number_id)
    return {"tarif": activated_tarif,
            "additions": activated_additions}
