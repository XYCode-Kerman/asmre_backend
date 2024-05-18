from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from database import engine
from models import Homework
from utils.auth.permission import require_permission, require_permission_depend
from utils.auth.user import get_user

router = APIRouter(prefix='/homework', tags=['作业管理'])


@router.get(
    '/',
    name='获取全部作业',
    response_model=List[Homework]
)
async def get_homeworks():
    return await engine.find(Homework)


@router.get(
    '/by/id/{homework_id}',
    name='根据ID获取作业',
    response_model=Homework | None
)
async def get_homework_by_id(homework_id: str):
    return await engine.find_one(Homework, Homework.id == ObjectId(homework_id))


@router.get(
    '/by/class/{class_id}',
    name='根据班级获取作业',
    response_model=List[Homework]
)
async def get_homeworks_by_class(class_id: str):
    return await engine.find(Homework, Homework.klass == ObjectId(class_id))


@router.post(
    '/',
    name='新增作业',
    description='需要 `/asmre/homework` 的 `create` 权限',
    response_model=Homework,
    dependencies=[
        Depends(require_permission_depend('/asmre/homework', 'create'))]
)
async def create_homework(homework: Homework):
    return await engine.save(homework)


@router.put(
    '/{homework_id}',
    name='更新作业',
    description='需要 `/asmre/homework/{homework_id}` 的 `write` 权限',
    response_model=Homework,
)
async def update_homework(homework_id: str, new_homework: Homework, user=Depends(get_user)):
    await require_permission(f'/asmre/homework/{homework_id}', 'write', user)
    existsing_homework = await engine.find_one(Homework, Homework.id == ObjectId(homework_id))

    if existsing_homework is None:
        raise HTTPException(status_code=404, detail='作业不存在')

    existsing_homework.model_update(new_homework, exclude=set(['id']))

    return await engine.save(existsing_homework)


@router.delete(
    '/{homework_id}',
    name='删除作业',
    description='需要 `/asmre/homework/{homework_id}` 的 `delete` 权限'
)
async def delete_homework(homework_id: str, user=Depends(get_user)):
    await require_permission(f'/asmre/homework/{homework_id}', 'delete', user)
    existsing_homework = await engine.find_one(Homework, Homework.id == ObjectId(homework_id))

    if existsing_homework is None:
        raise HTTPException(status_code=404, detail='作业不存在')

    await engine.delete(existsing_homework)

    return {'status': 'ok'}
