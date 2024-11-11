from typing import List

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth.schemas.client import ClientSchema
from src.auth.schemas.operator import OperatorSchema
from src.number.schemas.models import PhoneNumber
from src.database import Base


class Operator(Base):
    __tablename__ = 'operator'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=False)
    surname: Mapped[str] = mapped_column(Text, unique=False)
    email: Mapped[str] = mapped_column(Text)
    hashed_password: Mapped[str] = mapped_column(Text)

    def create_schema(self):
        return OperatorSchema(
            id=self.id,
            name=self.name,
            surname=self.surname,
            email=self.email,
            role="operator"
        )


class Client(Base):
    __tablename__ = 'client'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=False)
    surname: Mapped[str] = mapped_column(Text, unique=False)
    patronymic: Mapped[str] = mapped_column(Text, unique=False)
    contract_number: Mapped[str] = mapped_column(Text, unique=True)
    passport: Mapped[str] = mapped_column(Text, unique=True)
    hashed_password: Mapped[str] = mapped_column(Text)
    numbers: Mapped[List["PhoneNumber"]] = relationship()

    def create_schema(self, number: str):
        return ClientSchema(
            id=self.id,
            name=self.name,
            surname=self.surname,
            patronymic=self.patronymic,
            login_number=number,
            role="client"
        )

