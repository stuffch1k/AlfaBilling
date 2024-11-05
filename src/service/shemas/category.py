from typing import Optional

from pydantic import BaseModel, Field, ValidationError, root_validator, model_validator


class CreateSchema(BaseModel):
    name: str

class ReadSchema(CreateSchema):
    id: int

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