from typing import List

from sqlalchemy import Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship

Base = declarative_base()


class Operator(Base):
    __tablename__ = 'Operator'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(Text, unique=False)
    Surname: Mapped[str] = mapped_column(Text, unique=False)
    Email: Mapped[str] = mapped_column(Text)
    Hashed_password: Mapped[str] = mapped_column(Text)


class Client(Base):
    __tablename__ = 'Client'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(Text, unique=False)
    Surname: Mapped[str] = mapped_column(Text, unique=False)
    Patronymic: Mapped[str] = mapped_column(Text, unique=False)
    Contract_number: Mapped[str] = mapped_column(Text, unique=True)
    Passport: Mapped[str] = mapped_column(Text, unique=True)
    Hashed_password: Mapped[str] = mapped_column(Text)
    Numbers: Mapped[List["PhoneNumber"]] = relationship()


class PhoneNumber(Base):
    __tablename__ = 'Number'
    Id: Mapped[int] = mapped_column(primary_key=True)
    Phone_number: Mapped[str] = mapped_column(Text, unique=True)
    Balance: Mapped[float] = mapped_column(Float, default=0.0)
    Client_id: Mapped[int] = mapped_column(ForeignKey("Client.Id"))



