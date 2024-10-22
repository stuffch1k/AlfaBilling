from typing import List

from sqlalchemy import Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Operator(Base):
    __tablename__ = 'operator'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=False)
    surname: Mapped[str] = mapped_column(Text, unique=False)
    email: Mapped[str] = mapped_column(Text)
    hashed_password: Mapped[str] = mapped_column(Text)


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



