import random as rd

from fastapi import Depends, HTTPException
from src.number.repository.rest import RestRepository
from src.number.schemas.number import Choice, ChoiceSchema


class RestService:
    def __init__(self,rest_repository: RestRepository = Depends(RestRepository)):
        self.rest_repository = rest_repository

    def decrease_rests(self, choice: ChoiceSchema) -> None:
        """
        Тут вообще-то надо сделать общий интерфейс чтобы dry
        Но мне так влом
        """
        rows = self.rest_repository.get_all_rows()
        match choice.choice:
            case Choice.sms:
                self.decrease_sms(rows)
            case Choice.internet:
                self.decrease_internet(rows)
            case Choice.minute:
                self.decrease_minute(rows)
            case Choice.all:
                self.decrease_minute(rows)
                self.decrease_internet(rows)
                self.decrease_sms(rows)
            case _:
                raise HTTPException(status_code=403, detail='Invalid choice')

    def decrease_minute(self, rows):
        for row in rows:
            _minute = row.minute
            if _minute >= 1:
                try:
                    _minute -= rd.randint(1, int(_minute / 3))
                except ValueError:
                    _minute -= rd.randint(1, _minute)
                self.rest_repository.decrease_minute(row.number_id, _minute)

    def decrease_sms(self, rows):
        for row in rows:
            _sms = row.sms
            if _sms >= 1:
                try:
                    _sms -= rd.randint(1, int(_sms / 3))
                except ValueError:
                    _sms -= rd.randint(1, _sms)
                self.rest_repository.decrease_sms(row.number_id, _sms)

    def decrease_internet(self, rows):
        for row in rows:
            _internet = row.internet
            if _internet >= 1:
                try:
                    _internet -= rd.randint(1, int(_internet / 10))
                except ValueError:
                    _internet -= rd.randint(1, _internet)
                self.rest_repository.decrease_internet(row.number_id, _internet)


