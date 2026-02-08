from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post("/", response_model=schemas.EnrollmentOut)
def enroll(data: schemas.EnrollmentCreate, db: Session = Depends(get_db)):

    student = db.query(models.Student).filter(models.Student.id == data.student_id).first()
    course = db.query(models.Course).filter(models.Course.id == data.course_id).first()

    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")

    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == data.student_id,
        models.Enrollment.course_id == data.course_id,
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")

    enrollment = models.Enrollment(**data.dict())
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get("/", response_model=list[schemas.EnrollmentOut])
def list_enrollments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Enrollment).offset(skip).limit(limit).all()