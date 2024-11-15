from pydantic import BaseModel

class AddRestSchema(BaseModel):
    internet: int
    minute: int
    sms: int
    number_id: int