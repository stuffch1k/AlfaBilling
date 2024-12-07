from fastapi import Depends, HTTPException

from src.number.repository.number import NumberRepository
from src.number.repository.rest import RestRepository
from src.number.schemas.models import Activated, Rest
from src.number.schemas.number import AddServiceSchema
from src.service.repository.addition import AdditionRepository
from src.service.repository.addition_category import CategoryRepository
from src.service.repository.common_service import ServiceRepository
from src.service.repository.tarif import TarifRepository
from src.service.shemas.models import Tarif, Addition
from src.transaction.services.write_off import WriteOffService
from src.transaction.repository.write_off import WrifeOffRepository

class NumberService:
    def __init__(self, service_repository: ServiceRepository = Depends(ServiceRepository),
                 number_repository: NumberRepository = Depends(NumberRepository),
                 tarif_repository: TarifRepository = Depends(TarifRepository),
                 addition_repository: AdditionRepository = Depends(AdditionRepository),
                 rest_repository: RestRepository = Depends(RestRepository),
                 category_repository: CategoryRepository = Depends(CategoryRepository),
                 write_off_repository: WrifeOffRepository = Depends(WrifeOffRepository)):
        self.service_repository = service_repository
        self.number_repository = number_repository
        self.tarif_repository = tarif_repository
        self.addition_repository = addition_repository
        self.rest_repository = rest_repository
        self.category_repository = category_repository
        self.write_off_repository = write_off_repository

    def add_service(self, body: AddServiceSchema) -> None:
        '''
        Подключение услуги или тарифа
        Args:
            number: str
            service_id: int
        Returns None if 200 OK or raise possible exception
        '''
        if not self.existed_id(body.service_id):
            raise HTTPException(status_code=500,
                                detail=f"Service with pk {body.service_id} doesn't exist")
        if not self.existed_number(body.phone_number):
            raise HTTPException(status_code=500,
                                detail=f"Number {body.phone_number} doesn't exist")
        # проверяем, подключен ли у чипсика уже тариф
        # при этом дубли услуг подключать можно (5 пакетов по 1гб доп инета)
        is_tarif = self.is_tarif(body.service_id)
        if is_tarif and self.already_has_tarif(self.get_number_id(body.phone_number)):
            raise HTTPException(status_code=500,
                                detail=f"Number {body.phone_number} already has active tarif."
                                       f"Wanna change it?")

        number_id = self.get_number_id(body.phone_number)
        price = 0
        # идем добавлять то, что подключили к остаткам
        if is_tarif:
            _tarif = self.tarif_repository.get_tarif_by_id(body.service_id)
            self.add_rest(number_id,
                                 _tarif)
            price = _tarif.price
        else:
            _addition = self.addition_repository.get_addition_by_id(body.service_id)
            self.add_rest(number_id,
                                 _addition)
            price = _addition.price
        activated_id = self.number_repository.add_service(
            Activated(service_id=body.service_id, number_id=number_id))

        write_off_service = WriteOffService(self.number_repository, self.write_off_repository)
        write_off_service.create_write_off(number_id, activated_id, price)


    def get_rests(self, number: str):
        if not self.existed_number(number):
            raise HTTPException(status_code=500,
                                detail=f"Number {number} doesn't exist")
        number_id = self.get_number_id(number)
        return self.rest_repository.get_rests(number_id)


    def existed_id(self, service_id: int):
        id = self.service_repository.existed_id(service_id)
        if id is not None:
            return True
        else:
            return False

    def existed_number(self, number: str):
        number = self.number_repository.existed_number(number)
        if number is not None:
            return True
        else:
            return False

    def get_number_id(self, number: str) -> int:
        return self.number_repository.get_number_id(number)

    def is_tarif(self, service_id: int) -> bool:
        tarif = self.tarif_repository.get_tarif_by_id(service_id)
        return True if tarif is not None else False

    def already_has_tarif(self, number_id: int) -> bool:
        '''
        Check if client already has activated tarif
        Предполгаю
        Не может быть подключено несоклько тарифов на номере
        '''
        tarif_list = set(self.tarif_repository.get_tarifs_id())
        activated_ = set(self.number_repository.activated_list(number_id))
        tarif_id = tarif_list & activated_
        # пустой сет != None фанфакт
        return bool(tarif_id)


    def add_rest(self, number_id: int, body: Tarif | Addition):
        '''
        Добавляет то, что пришло к остаткам у абонента
        '''
        rest = Rest()
        # если подключен тариф - просто вливаем тариф
        # остатки при подключении или обновлении тарифа не переносим
        if type(body) is Tarif:
            rest = Rest(number_id=number_id, internet=body.internet,
                        is_unlimited_internet=body.is_unlimited_internet,
                        minute=body.minute,
                        sms=body.sms)
        else:
            # если подключена доп услуга
            # вычисляем категорию услуги
            category_name = self.category_repository.get_category_by_id(body.category_id)
            # получаем старые остатки
            rests = self.rest_repository.get_rests(number_id)
            match category_name.name:
                # исходя из категории плюсуем, тк пришло amount
                case "internet":
                    rest.internet = body.amount + rests.internet if rests is not None else 0
                    rest.minute = 0
                    rest.sms = 0
                case "minute":
                    rest.minute = body.amount + rests.minute if rests is not None else 0
                    rest.internet = 0
                    rest.sms = 0
                case "sms":
                    rest.sms = body.amount + rests.sms if rests is not None else 0
                    rest.internet = 0
                    rest.minute = 0
                case _:
                    # в случае различных роумингов, подписок, надо делать отдельный флаг
                    rest.sms = 0
                    rest.internet = 0
                    rest.minute = 0
            rest.is_unlimited_internet = body.is_unlimited
            rest.number_id = number_id
        self.rest_repository.add_or_update(rest)

