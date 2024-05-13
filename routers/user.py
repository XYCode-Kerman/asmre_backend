import datetime

from fastapi import APIRouter, Depends, HTTPException, Response

from database import engine
from models import TokenPayload, User
from utils import generate_token, get_user, hash_pwd, require_permission

router = APIRouter(prefix='/user', tags=['用户'])


@router.post('/register', name='注册', response_model=User)
async def register(user: User):
    if await engine.count(User, User.username == user.username or User.id == user.id) >= 1:
        raise HTTPException(status_code=400, detail='用户名或ID已存在')

    user.password = hash_pwd(user.password)

    return await engine.save(user)


@router.post('/login', name='登录', response_model=str)
async def login(username: str, password: str, response: Response):
    password = hash_pwd(password)
    user = await engine.find_one(User, User.username == username)

    if user is None:
        raise HTTPException(status_code=400, detail='用户名或密码错误')

    token = await generate_token(TokenPayload(
        username=user.username,
        exp=datetime.datetime.utcnow() + datetime.timedelta(days=15)
    ))

    response.set_cookie('xyuan-token', token, httponly=True)

    return token


@router.get('/me', name='获取用户信息', response_model=User)
async def me(user: User = Depends(get_user)):
    return user


@router.get('/check', name='检测权限', response_model=bool)
async def check_permission(resource: str, action: str, user: User = Depends(get_user)):
    await require_permission(resource, action, user)

    return True
