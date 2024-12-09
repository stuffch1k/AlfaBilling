from datetime import datetime

from pydantic import BaseModel, ConfigDict
from src.service.shemas.addition import ShortReadSchema as ShortAdditionSchema, FullReadSchema as FullAdditionSchema
from src.service.shemas.tarif import ShortReadSchema as ShortTarifSchema, FullReadSchema as FullTarifSchema


class ActivatedTarifShortSchema(ShortTarifSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ActivatedTarifFullSchema(FullTarifSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ActivatedAdditionShortSchema(ShortAdditionSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ActivatedAdditionFullSchema(FullAdditionSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ActivatedServiceSchema(BaseModel):
    activated_id: int = 0
    activation_date: datetime
    expiration_date: datetime | None = None
    service: (ActivatedAdditionShortSchema | ActivatedTarifShortSchema
              | ActivatedTarifFullSchema | ActivatedAdditionFullSchema) = None

    model_config = ConfigDict(from_attributes=True)



