from datetime import datetime, timedelta
from typing import List

from sqlalchemy import Text, Float, ForeignKey, Integer, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.transaction.schemas.models import Payment
from src.transaction.schemas.models import WriteOff


class PhoneNumber(Base):
    __tablename__ = 'number'
    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(Text, unique=True)
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    # отношения для того чтобы одним запросом тянуть из номера
    active_services: Mapped[List["Activated"]] = relationship()
    payments: Mapped[List["Payment"]] = relationship()
    write_off: Mapped[List["WriteOff"]] = relationship()


class Rest(Base):
    '''
    Таблица Остатки по услугам
    Номер 1 - 1 Остаток
    Вполне может быть атрибутом номера
    '''
    __tablename__ = "rest"
    internet: Mapped[int] = mapped_column(Integer)
    is_unlimited_internet: Mapped[bool] = mapped_column(Boolean, default=False)
    minute: Mapped[int] = mapped_column(Integer)
    sms: Mapped[int] = mapped_column(Integer)
    number_id: Mapped[int] = mapped_column(ForeignKey("number.id"), primary_key=True, autoincrement=False)

class Activated(Base):
    '''
    Подключенные на номере услуги из таблицы Service (тариф и допы)
    '''
    __tablename__ = "activated"
    id: Mapped[int] = mapped_column(primary_key=True)
    activation_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    expiration_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow()+timedelta(days=30))
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))
    number_id: Mapped[int] = mapped_column(ForeignKey("number.id"))


