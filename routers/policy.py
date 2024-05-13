from typing import List, Literal, Tuple

from fastapi import APIRouter, Depends

from utils.auth.csb import enforcer
from utils.auth.permission import require_permission_depend

router = APIRouter(prefix='/policy', tags=['权限策略'])


@router.get(
    '/policy',
    name='获取所有权限策略',
    response_model=List[Tuple[str, str, str]],
    responses={
        200: {
            'description': '成功获取',
            'content': {
                'application/json': {
                    'example': [
                        ['sub', 'obj', 'act']
                    ]
                }
            }
        }
    },
    dependencies=[Depends(require_permission_depend('/policy', 'read'))],
    description='需要 `/policy` 的 `read` 权限'
)
async def get_all_policies():
    return enforcer.get_policy()


@router.post(
    '/policy',
    name='添加权限策略',
    response_model=bool,
    dependencies=[Depends(require_permission_depend('/policy', 'write'))],
    description='需要 `/policy` 的 `write` 权限'
)
async def add_policy(policy: Tuple[str, str, str]):
    result = enforcer.add_policy(*policy)

    return result


@router.delete(
    '/policy',
    name='删除权限策略',
    response_model=Literal['ok'],
    dependencies=[Depends(require_permission_depend('/policy', 'delete'))],
    description='需要 `/policy` 的 `delete` 权限'
)
async def delete_policy(policy: Tuple[str, str, str]):
    enforcer.remove_policy(*policy)

    return 'ok'


@router.get(
    '/roles',
    name='获取所有角色',
    response_model=List[str],
    dependencies=[Depends(require_permission_depend('/role', 'read'))]
)
async def get_roles():
    return enforcer.get_all_roles()


@router.get(
    '/role/{username}',
    name='获取用户角色',
    response_model=List[str],
    dependencies=[Depends(require_permission_depend('/role', 'read'))]
)
async def get_role_for_user(username: str):
    return enforcer.get_roles_for_user(username)


@router.post(
    '/role/{username}',
    name='添加角色',
    response_model=bool,
    dependencies=[Depends(require_permission_depend('/role', 'write'))]
)
async def add_role(username: str, role: str):
    return enforcer.add_role_for_user(username, role)


@router.delete(
    '/role/{username}',
    name='删除角色',
    response_model=Literal['ok'],
    dependencies=[Depends(require_permission_depend('/role', 'delete'))]
)
async def delete_role(username: str, role: str):
    enforcer.delete_role_for_user(username, role)

    return 'ok'
