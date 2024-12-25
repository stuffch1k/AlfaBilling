from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from src.transaction.schemas.models import WriteOff

class DateFilterSchema(BaseModel):
    number_id: int
    date_start: datetime = Field(default=datetime.today() - timedelta(days=30))
    date_end: datetime = Field(default=datetime.today())

class ReadSchema(BaseModel):
    activated_id: int
    price: float
    date: datetime

class FullReadSchema(BaseModel):
    name: str
    date: datetime
    amount: float
    price: float
