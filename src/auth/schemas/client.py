from pydantic import BaseModel, ConfigDict


class ClientBaseSchema(BaseModel):
    name: str
    surname: str
    patronymic: str


class ClientCreateSchema(ClientBaseSchema):
    """
    Pydantic модель клиента для регистрации

    Attributes
    ----------
    name: str
        имя
    surname: str
        фамилия
    patronymic: str
        отчество
    number: str
        номер телефона
    contract_number: str
        номер договора
    passport: str
        номер паспорта
    password: str
        пароль
    """
    number: str
    contract_number: str
    passport: str
    password: str


class ClientLoginSchema(BaseModel):
    """
    Pydantic модель клиента для входа

    Attributes
    ----------
    number: str
        номер телефона
    password: str
        пароль
    """
    number: str
    password: str


class ClientSchema(ClientBaseSchema):
    """
    Pydantic модель клиента

    Attributes
    ----------
    id: int
        id клиента из бд
    login_number: str
        номер
    name: str
        имя
    surname: str
        фамилия
    patronymic: str
        отчество
    role: str
        роль "client"
    """
    id: int
    login_number: str = None
    role: str = "client"
    model_config = ConfigDict(from_attributes=True)


