from fastapi import Depends, HTTPException

from models import User

from .csb import enforcer
from .user import get_user


async def require_permission(resource: str, action: str, user: User = Depends(get_user)) -> User:
    if enforcer.enforce(user.username, resource, action):
        return user
    else:
        raise HTTPException(status_code=403, detail="禁止访问，没有权限")


def require_permission_depend(resource: str, action: str):
    async def wrapper(user: User = Depends(get_user)) -> User:
        return await require_permission(resource, action, user)

    return wrapper
