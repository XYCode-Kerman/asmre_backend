from odmantic import Model, Reference

from .klass import Klass
from .user import User


class Student(Model):
    name: str
    school_class: Klass = Reference()
    user: User = Reference()
