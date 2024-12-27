from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.number.schemas.number import NumberInfoSchema


class ClientInfoSchema(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str
    number: str = None

    model_config = ConfigDict(from_attributes=True)


class ClientShortSchema(ClientInfoSchema):
    """
    For clients list
    """
    tarif_name: str = None
    balance: float = None


class ClientFullSchema(BaseModel):
    client_info: ClientInfoSchema
    number_info: NumberInfoSchema

class ClientFilterSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    phone_number: Optional[str] = None

