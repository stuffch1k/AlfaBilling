from pydantic import BaseModel


class ShortReadSchema(BaseModel):
    name: str
    price: float
    amount: float
    is_unlimited: bool

class CreateSchema(ShortReadSchema):
    description: str
    duration: int
    category_id: int

class UpdateSchema(BaseModel):
    price: float
    amount: float
    is_unlimited: bool
    description: str

class FullReadSchema(CreateSchema):
    pass

class AdditionReadSchema(ShortReadSchema):
    service_id: int


