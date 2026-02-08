from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("/", response_model=schemas.CourseOut)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):

    duplicate = db.query(models.Course).filter(models.Course.title == course.title).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Course already exists")

    db_course = models.Course(title=course.title)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get("/", response_model=list[schemas.CourseOut])
def list_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Course).offset(skip).limit(limit).all()


@router.put("/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, data: schemas.CourseCreate, db: Session = Depends(get_db)):

    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    duplicate = db.query(models.Course).filter(
        models.Course.title == data.title,
        models.Course.id != course_id,
    ).first()

    if duplicate:
        raise HTTPException(status_code=400, detail="Course title already exists")

    course.title = data.title
    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):

    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(course)
    db.commit()
    return {"message": "Course deleted"}