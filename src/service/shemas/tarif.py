from pydantic import BaseModel


class CreateSchema(BaseModel):
    name: str
    description: str
    price: float
    duration: int
    internet: int
    is_unlimited_internet: bool
    minute: int
    sms: int

class UpdateSchema(BaseModel):
    price: float
    internet: int
    is_unlimited_internet: bool
    minute: int
    sms: int

class ShortReadSchema(UpdateSchema):
    name: str

class FullReadSchema(CreateSchema):
    pass


