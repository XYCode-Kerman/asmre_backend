from odmantic import Model
from pydantic import BaseModel


class Klass(Model):
    name: str
    description: str


class KlassStats(BaseModel):
    total_students: int
    total_credit_updates: int
    average_credit: float
