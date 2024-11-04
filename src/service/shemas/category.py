from pydantic import BaseModel


class CreateSchema(BaseModel):
    name: str

class ReadSchema(CreateSchema):
    id: int