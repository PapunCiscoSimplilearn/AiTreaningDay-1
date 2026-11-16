from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Department, Student
from schemas import StudentCreate, StudentOut


router = APIRouter(prefix="/api/students", tags=["students"])


@router.get("/", response_model=list[StudentOut])
def get_students(db: Annotated[Session, Depends(get_db)]):
    statement = (
        select(Student)
        .options(joinedload(Student.department))
        .order_by(Student.student_id)
    )
    return db.scalars(statement).all()


@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Annotated[Session, Depends(get_db)]):
    department = db.get(Department, payload.department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    student = Student(**payload.model_dump(), department=department)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student