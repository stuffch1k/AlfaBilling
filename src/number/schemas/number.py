from pydantic import BaseModel, Field
from enum import Enum


class Choice(str, Enum):
    internet = 'internet'
    minute = 'minute'
    sms = 'sms'
    all = 'all'
class AddServiceSchema(BaseModel):
    service_id: int
    phone_number: str

class ChoiceSchema(BaseModel):
    choice: Choice = Field(default=Choice.all)
    class Config:
        use_enum_values = True

