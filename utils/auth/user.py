import hashlib

import jwt
from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyCookie

from config import SECRET
from database import engine
from models import TokenPayload, User

apikey_schema = APIKeyCookie(name="xyuan-token", auto_error=True)


async def generate_token(payload: TokenPayload):
    return jwt.encode(
        payload.model_dump(),
        SECRET,
        algorithm="HS256"
    )


async def decode_token(token: str = Depends(apikey_schema)) -> TokenPayload:
    try:
        return TokenPayload.model_validate(jwt.decode(token, SECRET, algorithms=["HS256"]))
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=403, detail="Token 错误。原始错误：" + str(e))


async def get_user(payload: TokenPayload = Depends(decode_token)) -> User:
    user = await engine.find_one(User, User.username == payload.username)

    if user is None:
        raise HTTPException(status_code=403, detail="用户不存在")

    return user


def hash_pwd(pwd: str) -> str:
    return hashlib.sha512(hashlib.sha256(pwd.encode('utf-8')).digest() + SECRET.encode('utf-8')).hexdigest()
