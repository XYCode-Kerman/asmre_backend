import decimal

from odmantic import Model, Reference

from database import engine

from .klass import Klass
from .user import User


class Student(Model):
    name: str
    school_class: Klass = Reference()
    user: User = Reference()
    credit: float = -1

    async def compute_credit(self) -> float:
        from models.credits import CreditUpdate

        credit_updates = await engine.find(CreditUpdate, CreditUpdate.student == self.id)

        add_sum = sum([decimal.Decimal(str(update.number))
                       for update in credit_updates if update.type == 'add'])
        reduce_sum = sum([decimal.Decimal('-' + str(update.number))
                          for update in credit_updates if update.type == 'reduce'])

        credit_sum = add_sum + reduce_sum

        self.credit = float(credit_sum)

        return float(credit_sum)
