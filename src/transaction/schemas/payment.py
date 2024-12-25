from datetime import datetime
from pydantic import BaseModel, Field

from src.transaction.schemas.write_off import DateFilterSchema as FilterSchema


class ReadSchema(BaseModel):
    amount: float
    date: datetime

class FullReadSchema(ReadSchema):
    name: str = Field(default='Пополнение')

class CreateSchema(ReadSchema):
    number_id: int
    date: datetime = Field(default=datetime.today())

class DateFilterSchema(FilterSchema):
    pass



