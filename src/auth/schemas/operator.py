from pydantic import BaseModel, ConfigDict


class OperatorLoginSchema(BaseModel):
    Email: str
    Password: str


class OperatorBaseSchema(BaseModel):
    Name: str
    Surname: str
    Email: str


class OperatorCreateSchema(OperatorBaseSchema):
    Password: str


class OperatorSchema(OperatorBaseSchema):
    Id: int
    Role: str = "operator"

    model_config = ConfigDict(from_attributes=True)
