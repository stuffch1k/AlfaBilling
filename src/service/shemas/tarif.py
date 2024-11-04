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


class ShortReadSchema(BaseModel):
    name: str
    price: float
    internet: int
    is_unlimited_internet: bool
    minute: int
    sms: int

class FullReadSchema(CreateSchema):
    pass


