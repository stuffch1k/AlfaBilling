from fastapi import Depends
from sqlalchemy.orm import Session

from ...models import Operator
from ...database import database


class OperatorRepository:

    def __init__(self, session: Session = Depends(database.get_session)) -> None:
        self.session = session

    def add_operator_to_db(self, operator: Operator):
        self.session.add(operator)
        self.session.commit()
        self.session.refresh(operator)

    def find_operator_by_email(self, email: str) -> Operator | None:
        operator = self.session.query(Operator).filter(Operator.Email == email).first()
        return operator

    def get_operator_by_id(self, operator_id: int) -> Operator | None:
        operator = self.session.query(Operator).get(operator_id)
        return operator
