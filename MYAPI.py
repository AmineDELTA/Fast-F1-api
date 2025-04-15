from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional
from fastapi import Query

app = FastAPI(title="My API", description="This API does cool stuff", version="1.0.0")

students = {1: {"name": "los_pipitas", "age": 245, "year": "12BC"}}


class Student(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/get-student/{student_id}")
async def get_student_id(
    student_id: int = Path(description="the student ID", gt=0, it=3)
):
    return students[student_id]


@app.get("/get-by-name")
def get_student_name(name: str = Query(default=None, max_length=50)):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}


@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student already exists."}

    students[student_id] = student
    return students[student_id]


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    if student.name is not None:
        students[student_id]["name"] = student.name

    if student.age is not None:
        students[student_id]["age"] = student.age

    if student.year is not None:
        students[student_id]["year"] = student.year

    return students[student_id]
