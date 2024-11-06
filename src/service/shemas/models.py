from sqlalchemy import String, Text, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class AdditionCategory(Base):
    '''
    Таблица Категории создается для фильтрации Дополнительных услуг.
    '''
    __tablename__ = 'addition_category'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(260), unique=True)

class Service(Base):
    '''
    Услуга - родитель Тарифа и Допов.
    Тут должно было быть наследование, но SQLA не умеет.
    id - идентификатор услуги, автоинкремент.
    При создании записи в этой таблице обязательно передать параметр потомкам.
    Дискриминатор потомков "виртуальный".
    '''
    __tablename__ = 'service'
    id: Mapped[int] = mapped_column(primary_key=True)
    __mapper_args__ = {
    'polymorphic_identity': 'service',
    }

class Tarif(Service):
    __tablename__ = 'tarif'
    # первичный внешний ключ wtf - обеспечение целостности
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"), primary_key=True, autoincrement=False)
    # общие аттрибуты услуги
    # тариф их как бы наследует
    name: Mapped[str] = mapped_column(String(260), unique=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)
    duration: Mapped[int] = mapped_column(Integer)
    # уникальные поля сущности Тариф
    internet: Mapped[int] = mapped_column(Integer)
    is_unlimited_internet: Mapped[bool] = mapped_column(Boolean, default=False)
    minute: Mapped[int] = mapped_column(Integer)
    sms: Mapped[int] = mapped_column(Integer)
    __mapper_args__ = {
    'polymorphic_identity': 'tarif',
    }

class Addition(Service):
    __tablename__ = "addition"
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"), primary_key=True, autoincrement=False)
    # наследуемые поля
    name: Mapped[str] = mapped_column(String(260))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)
    duration: Mapped[int] = mapped_column(Integer)
    # уникальные поля
    amount: Mapped[float] = mapped_column(Float)
    is_unlimited: Mapped[bool] = mapped_column(Boolean, default=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("addition_category.id"))
    __mapper_args__ = {
    'polymorphic_identity': 'addition',
    }