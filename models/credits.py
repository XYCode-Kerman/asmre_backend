import datetime
from typing import Literal

from odmantic import Model, Reference

from .student import Student


class CreditUpdate(Model):
    type: Literal['add', 'reduce']
    number: float
    student: Student = Reference()
    reason: str
    create_time: datetime.datetime
    update_time: datetime.datetime
