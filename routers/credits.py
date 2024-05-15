import datetime
import decimal
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from database import engine
from models import CreditUpdate, Student
from utils import get_user, require_permission

router = APIRouter(prefix='/credit', tags=['积分管理'])


@router.get('/', response_model=List[CreditUpdate], name='获取积分变更记录')
async def get_credit_updates():
    return await engine.find(CreditUpdate)


@router.post('/', response_model=CreditUpdate, name='创建积分变更记录', description='需要 `/asmre/credit/{student_name}` 的 `create` 权限')
async def create_credit_update(update: CreditUpdate, user=Depends(get_user)):
    await require_permission(f'/asmre/credit/{update.student.name}', 'create', user)

    update.create_time = datetime.datetime.utcnow()

    return await engine.save(update)


@router.put('/{id}', response_model=CreditUpdate, name='更新积分变更记录', description='需要 `/asmre/credit/{student_name}` 的 `write` 权限')
async def update_credit_update(id: str, update: CreditUpdate, user=Depends(get_user)):
    await require_permission(f'/asmre/credit/{update.student.name}', 'write', user)

    credit_update = await engine.find_one(CreditUpdate, CreditUpdate.id == ObjectId(id))

    if credit_update is None:
        raise HTTPException(status_code=404, detail='积分变更记录不存在')

    credit_update.model_update(update, exclude=set([
        'id', 'create_time', 'update_time']))
    credit_update.update_time = datetime.datetime.utcnow()

    return await engine.save(credit_update)


@router.delete('/{id}', name='删除积分变更记录', description='需要 `/asmre/credit/{student_name}` 的 `delete` 权限')
async def delete_credit_update(id: str, user=Depends(get_user)):
    await require_permission(f'/asmre/credit/{id}', 'delete', user)

    credit_update = await engine.find_one(CreditUpdate, CreditUpdate.id == ObjectId(id))

    if credit_update is None:
        raise HTTPException(status_code=404, detail='积分变更记录不存在')

    await engine.delete(credit_update)

    return {
        'status': 'ok'
    }


@router.get('/{student_name}', name='获取学生积分变更记录', response_model=List[CreditUpdate])
async def get_student_credit_updates(student_name: str):
    student = await engine.find_one(Student, Student.name == student_name)

    if student is None:
        return []

    return await engine.find(CreditUpdate, CreditUpdate.student == student.id)


@router.get('/{student_name}/credit', name='获取学生积分', response_model=float)
async def get_student_credit(student_name: str) -> float:
    student = await engine.find_one(Student, Student.name == student_name)

    if student is None:
        return -1

    credit_updates = await engine.find(CreditUpdate, CreditUpdate.student == student.id)

    add_sum = sum([decimal.Decimal(str(update.number))
                  for update in credit_updates if update.type == 'add'])
    reduce_sum = sum([decimal.Decimal('-' + str(update.number))
                     for update in credit_updates if update.type == 'reduce'])

    credit_sum = add_sum + reduce_sum

    return float(credit_sum)
