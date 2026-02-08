from pydantic import BaseModel
from typing import List


class StudentBase(BaseModel):
    name: str


class StudentCreate(StudentBase):
    pass


class StudentOut(StudentBase):
    id: int

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    title: str


class CourseCreate(CourseBase):
    pass


class CourseOut(CourseBase):
    id: int

    class Config:
        from_attributes = True


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentOut(BaseModel):
    id: int
    student_id: int
    course_id: int

    class Config:
        from_attributes = True