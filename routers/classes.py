from decimal import Decimal
from typing import Dict, List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from database import engine
from models import CreditUpdate, Klass, KlassStats, Student
from utils import get_user, require_permission, require_permission_depend

router = APIRouter(prefix='/classes', tags=['班级管理'])

NO_CLASS_RESPONSE = {
    'description': '班级不存在',
    'content': {
        'application/json': {
            'example': {
                'detail': '班级不存在'
            }
        }
    }
}


@router.get('/', name='获取班级列表', response_model=List[Klass])
async def get_classes():
    return await engine.find(Klass)


@router.post('/', name='创建班级', response_model=Klass, description='需要 `/asmre/class` 的 `create` 权限', dependencies=[Depends(require_permission_depend('/asmre/class', 'create'))])
async def create_class(klass: Klass):
    return await engine.save(klass)


@router.put('/{object_id}', name='更新班级', response_model=Klass, responses={
    404: NO_CLASS_RESPONSE
}, description='需要 `/asmre/class/{object_id}` 的 `write` 权限')
async def update_class(object_id: str, klass_new: Klass, user=Depends(get_user)):
    await require_permission(f'/asmre/class/{object_id}', 'write', user)
    klass = await engine.find_one(Klass, Klass.id == ObjectId(object_id))

    if klass is None:
        raise HTTPException(status_code=404, detail='班级不存在')

    klass.model_update(klass_new, exclude=set('id'))

    return await engine.save(klass)


@router.delete('/{object_id}', name='删除班级', responses={
    200: {
        'description': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'status': 'ok'
                }
            }
        }
    },
    404: NO_CLASS_RESPONSE
}, description='需要 `/asmre/class/{object_id}` 的 `delete` 权限')
async def delete_class(object_id: str, user=Depends(get_user)):
    await require_permission(f'/asmre/class/{object_id}', 'delete', user)

    klass = await engine.find_one(Klass, Klass.id == ObjectId(object_id))

    if klass is None:
        raise HTTPException(status_code=404, detail='班级不存在')

    await engine.delete(klass)

    return {
        'status': 'ok'
    }


@router.get('/stats/{object_id}', name='获取班级基本情况', response_model=KlassStats)
async def get_stats(object_id: str):
    klass = await engine.find_one(Klass, Klass.id == ObjectId(object_id))

    if klass is None:
        raise HTTPException(status_code=404, detail='班级不存在')

    students = await engine.find(Student, Student.school_class == klass.id)
    credit_updates = await engine.find(CreditUpdate, CreditUpdate.student.in_([s.id for s in students]))
    student_credits: Dict[str, Decimal] = {}

    for credit_update in credit_updates:
        student_credits[credit_update.student.name] = student_credits.get(credit_update.student.name, Decimal(
            0)) + (Decimal(str(credit_update.number)) if credit_update.type == 'add' else Decimal('-' + str(credit_update.number)))

    return KlassStats(
        total_students=students.__len__(),
        total_credit_updates=credit_updates.__len__(),
        average_credit=float(sum(student_credits.values()) /
                             students.__len__() if students.__len__() > 0 else Decimal('0')),
    )
