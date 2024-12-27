from pydantic import BaseModel, Field
from enum import Enum

from src.number.schemas.activated import ActivatedServiceSchema
from src.number.schemas.rest import RestSchema


class Choice(str, Enum):
    internet = 'internet'
    minute = 'minute'
    sms = 'sms'
    all = 'all'


class ChoiceSchema(BaseModel):
    choice: Choice = Field(default=Choice.all)
    class Config:
        use_enum_values = True


class AddServiceSchema(BaseModel):
    service_id: int
    phone_number: str


class AddNumberSchema(BaseModel):
    phone_number: str


class NumberInfoSchema(BaseModel):
    id: int
    client_id: int
    balance: float = None
    rests: RestSchema | None = None
    activated_tarif: ActivatedServiceSchema | None = None
    activated_additions: list[ActivatedServiceSchema] = None


class DeactivateServiceSchema(BaseModel):
    activated_id: int
    phone_number: str


class ChangeTarifSchema(BaseModel):
    tarif_id: int
    phone_number: str

