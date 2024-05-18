from datetime import datetime
from typing import Any, List, Literal

from odmantic import Model, Reference

from .student import Student


class TaskAction(Model):
    action: Literal['add_credit', 'reduce_credit']
    data: Any
    completed: bool = False


class Task(Model):
    student: Student = Reference()
    content: str
    deadline: datetime
    completed: bool = False
    actions_when_completed: List[TaskAction] = []
    actions_when_not_completed: List[TaskAction] = []
