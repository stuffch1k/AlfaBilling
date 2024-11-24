from datetime import datetime
from typing import List

from sqlalchemy import Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class WriteOff(Base):
    '''
    Таблица списаний за какую-то услугу (тариф или допик)
    '''
    __tablename__ = 'write_off'
    id: Mapped[int] = mapped_column(primary_key=True)
    # цена - idk почему не прайс
    amount: Mapped[str] = mapped_column(Float, default=0)
    date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    activated_id: Mapped[int] = mapped_column(ForeignKey("activated.id"))
    number_id: Mapped[int] = mapped_column(ForeignKey("number.id"))


class Payment(Base):
    '''
    Таблица пополненений
    '''
    __tablename__ = 'payment'
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[str] = mapped_column(Float, default=0)
    date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    number_id: Mapped[int] = mapped_column(ForeignKey("number.id"))