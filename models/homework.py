from datetime import datetime

from odmantic import Model, Reference

from .klass import Klass


class Homework(Model):
    subject: str
    name: str
    description: str
    starttime: datetime
    deadline: datetime
    klass: Klass = Reference()
