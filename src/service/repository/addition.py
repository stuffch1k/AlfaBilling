from fastapi import Depends
from sqlalchemy.orm import Session

from ..shemas.models import Addition
from ...database import database


class AdditionRepository:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session = session

