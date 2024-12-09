from pydantic import BaseModel, ConfigDict


class RestSchema(BaseModel):
    internet: int
    minute: int
    sms: int

    model_config = ConfigDict(from_attributes=True)


class AddRestSchema(RestSchema):
    number_id: int
