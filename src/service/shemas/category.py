from typing import Optional

from pydantic import BaseModel, Field, ValidationError, root_validator, model_validator


TYPES = {
    'internet': 'Интернет',
    'sms': 'СМС',
    'minute': 'Звонки',
    'finance': 'Финансы',
    'online cinema': 'Онлайн-кинотеатры'
}

class CreateSchema(BaseModel):
    name: str

class ReadSchema(CreateSchema):
    id: int

class FullReadSchema(ReadSchema):
    count: int
    ru_name: str

class ChooseSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)

    class Config:
        validate_assignment = True

    @model_validator(mode='after')
    def validate_xor(self):
        if not self.id and not self.name:
            raise ValidationError('Either id or name must be set.')
        return self