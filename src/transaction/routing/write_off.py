from fastapi import APIRouter, Depends

from src.auth.permissions import permissions
from src.number.services.activated import ActivatedService
from src.service.services.common_service import CommonService
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
async def emulate_write_off(write_off_service: WriteOffService = Depends(),
                      activated_service: ActivatedService = Depends(),
                      common_service: CommonService = Depends()
                      ):
    """
    Эта фича будет кроном- пока для удобства эндпоинт
    1. Бежим по таблице activated:
        смотрим дату - если сегодня
        получаем id, service_id, number_id
    2. Идем получать стоимость услуг и длительность по service_id - хорошо бы формировать словарь
    3. Идем в number или activated service
    4. Пишем что-то типа update_activated
        Оттуда адим списания
        Обновляем activated
    """
    today_activated_services: list[tuple] = activated_service.get_today_service()
    services = list(set([el[1] for el in today_activated_services]))
    service_prices = common_service.get_service_price(services)
    service_duration = common_service.get_service_duration(services)
    activated_service.update_activated(today_activated_services, service_duration)
    write_off_service.create_write_off_list(today_activated_services, service_prices)


