from fastapi import Depends
from sqlalchemy.orm import Session

from ..shemas.models import Service
from ...database import database

class ServiceRepository:
    def __init__(self, session: Session = Depends(database.get_session)) -> None:
        self.session = session

    def create_service_key(self) -> int:
        service_key = Service()
        self.session.add(service_key)
        self.session.flush()
        self.session.refresh(service_key)
        pk = service_key.id
        return pk
