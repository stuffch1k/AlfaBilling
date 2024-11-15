from pydantic import BaseModel

class AddServiceSchema(BaseModel):
    service_id: int
    phone_number: str
