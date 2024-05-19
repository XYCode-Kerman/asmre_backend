from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from database import engine
from models import Student, Task
from utils.auth.permission import require_permission, require_permission_depend
from utils.auth.user import get_user

router = APIRouter(prefix='/task', tags=['任务管理'])
DESCRIPTION_ABOUT_TASK = '任务不同于作业，任务是针对于学生的，而作业是布置给全班的。任务还可以设置正常完成时应做的操作（例如加分）和没完成时的操作（例如减分）。'


@router.get(
    '/',
    name='获取全部任务',
    description=DESCRIPTION_ABOUT_TASK,
    response_model=List[Task]
)
async def get_tasks():
    return await engine.find(Task)


@router.get(
    '/by/student/id/{student_id}',
    name='根据学生ID获取任务',
    description=DESCRIPTION_ABOUT_TASK,
    response_model=List[Task]
)
async def get_tasks_by_student_id(student_id: str):
    return await engine.find(Task, Task.student == ObjectId(student_id))


@router.get(
    '/by/student/name/{student_name}',
    name='根据学生姓名获取任务',
    description=DESCRIPTION_ABOUT_TASK,
    response_model=List[Task]
)
async def get_tasks_by_student_name(student_name: str):
    student = await engine.find_one(Student, Student.name == student_name)

    return await engine.find(Task, Task.student == student.id)


@router.get(
    '/by/id/{task_id}',
    name='根据ID获取任务',
    description=DESCRIPTION_ABOUT_TASK,
    response_model=Task | None
)
async def get_task_by_id(task_id: str):
    return await engine.find_one(Task, Task.id == ObjectId(task_id))


@router.post(
    '/',
    name='新增任务',
    description=f'{DESCRIPTION_ABOUT_TASK}\n需要 `/asmre/task` 的 `create` 权限',
    response_model=Task,
    dependencies=[Depends(require_permission_depend('/asmre/task', 'create'))]
)
async def create_task(task: Task):
    return await engine.save(task)


@router.put(
    '/{task_id}',
    name='更新任务',
    description=DESCRIPTION_ABOUT_TASK +
    '\n需要 `/asmre/task/{task_id}` 的 `write` 权限',
    response_model=Task
)
async def update_task(task_id: str, new_task: Task, user=Depends(get_user)):
    await require_permission(f'/asmre/task/{task_id}', 'write', user)
    existing_task = await engine.find_one(Task, Task.id == ObjectId(task_id))

    if existing_task is None:
        raise HTTPException(status_code=404, detail='任务不存在')

    existing_task.model_update(new_task, exclude=set(['id']))

    return await engine.save(existing_task)


@router.delete(
    '/{task_id}',
    name='删除任务',
    description=DESCRIPTION_ABOUT_TASK +
    '\n需要 `/asmre/task/{task_id}` 的 `delete` 权限'
)
async def delete_task(task_id: str, user=Depends(get_user)):
    await require_permission(f'/asmre/task/{task_id}', 'delete', user)
    existing_task = await engine.find_one(Task, Task.id == ObjectId(task_id))

    if existing_task is None:
        raise HTTPException(status_code=404, detail='任务不存在')

    await engine.delete(existing_task)

    return {'status': 'ok'}
