from pydantic import BaseModel

from src.number.schemas.activated import ActivatedServiceSchema
from src.number.schemas.rest import RestSchema


class AddServiceSchema(BaseModel):
    service_id: int
    phone_number: str


class AddNumberSchema(BaseModel):
    phone_number: str


class NumberInfoSchema(BaseModel):
    id: int
    client_id: int
    balance: float = None
    rests: RestSchema = None
    activated_tarif: ActivatedServiceSchema | None = None
    activated_additions: list[ActivatedServiceSchema] = None


class DeactivateServiceSchema(BaseModel):
    activated_id: int
    phone_number: str
