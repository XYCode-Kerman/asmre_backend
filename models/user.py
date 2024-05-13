import datetime

from odmantic import Model
from pydantic import BaseModel


class User(Model):
    username: str
    nickname: str
    avatar: str
    password: str


class TokenPayload(BaseModel):
    username: str
    exp: datetime.datetime
