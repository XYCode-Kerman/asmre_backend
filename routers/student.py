import asyncio
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from database import engine
from models import Student
from utils import get_user, require_permission, require_permission_depend

router = APIRouter(prefix="/student", tags=["学生管理"])


@router.get('/', name="获取学生列表", response_model=List[Student])
async def get_students():
    students = await engine.find(Student)

    await asyncio.gather(*[student.compute_credit() for student in students], return_exceptions=True)

    students.sort(key=lambda x: x.credit, reverse=True)

    return students


@router.get('/by/class/{class_id}', name="获取班级学生列表", response_model=List[Student])
async def get_students_by_class(class_id: str):
    students = await engine.find(Student, Student.school_class == ObjectId(class_id))

    await asyncio.gather(*[student.compute_credit() for student in students], return_exceptions=True)

    students.sort(key=lambda x: x.credit, reverse=True)

    return students


@router.get('/by/name/{student_name}', name="获取同名学生", response_model=List[Student])
async def get_students_by_name(student_name: str):
    students = await engine.find(Student, Student.name == student_name)

    await asyncio.gather(*[student.compute_credit() for student in students], return_exceptions=True)
    students.sort(key=lambda x: x.credit, reverse=True)

    return students


@router.post('/', name="创建学生", dependencies=[Depends(require_permission_depend('/asmre/student', 'create'))], response_model=Student, description='需要 `/asmre/student` 的 `create` 权限')
async def create_student(student: Student):
    await student.compute_credit()
    return await engine.save(student)


@router.put('/{student_id}', name="更新学生", response_model=Student, description='需要 `/asmre/student/{student_id}` 的 `update` 权限')
async def update_student(student_id: str, student_new: Student, user=Depends(get_user)):
    await require_permission(f'/asmre/student/{student_id}', 'update', user)

    student = await engine.find_one(Student, Student.id == ObjectId(student_id))

    if student is None:
        raise HTTPException(status_code=404, detail="学生不存在")

    await student.compute_credit()

    student.model_update(student_new, exclude=set('id'))

    return await engine.save(student_new)


@router.delete('/{student_id}', name="删除学生", description='需要 `/asmre/student/{student_id}` 的 `delete` 权限')
async def delete_student(student_id: str, user=Depends(get_user)):
    await require_permission(f'/asmre/student/{student_id}', 'delete', user)

    student = await engine.find_one(Student, Student.id == ObjectId(student_id))

    if student is None:
        raise HTTPException(status_code=404, detail="学生不存在")

    await engine.delete(student)

    return {
        'status': 'ok'
    }
