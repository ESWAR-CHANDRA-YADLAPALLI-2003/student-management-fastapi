from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(name=student.name)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.get("/", response_model=list[schemas.StudentOut])
def list_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Student).offset(skip).limit(limit).all()


@router.put("/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, data: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = data.name
    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": "Student deleted"}