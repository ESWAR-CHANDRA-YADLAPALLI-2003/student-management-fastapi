from fastapi import FastAPI

from .database import Base, engine
from .routers import students, courses, enrollments

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None, redoc_url=None)  # 🔒 hide docs in production


@app.get("/")
def home():
    return {"message": "Student Management API with Database"}


app.include_router(students.router)
app.include_router(courses.router)
app.include_router(enrollments.router)