from pydantic import BaseModel, ConfigDict


class ClientBaseSchema(BaseModel):
    Name: str
    Surname: str
    Patronymic: str


class ClientCreateSchema(ClientBaseSchema):
    Number: str
    Contract_number: str
    Passport: str
    Password: str


class ClientLoginSchema(BaseModel):
    Number: str
    Password: str


class ClientSchema(ClientBaseSchema):
    Id: int
    Role: str = "client"
    model_config = ConfigDict(from_attributes=True)


