import math

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="GitHub Copilot Runtime Debugging Lab")


class Employee(BaseModel):
    name: str
    age: int
    salary: float


# ------------------------------------------------
# ERROR 1: TypeError
# ------------------------------------------------

@app.get("/employee/bonus")
def calculate_bonus():

    salary = 50000.0

    bonus = salary * 0.10

    return {"bonus": bonus}



# ------------------------------------------------
# ERROR 3: ZeroDivisionError
# ------------------------------------------------

@app.get("/employee/average-salary")
def calculate_average_salary(
    total_salary: float = 150000,
    employee_count: int = 3
):

    if employee_count <= 0:
        raise HTTPException(
            status_code=400,
            detail="Employee count must be greater than zero"
        )

    if not math.isfinite(total_salary):
        raise HTTPException(
            status_code=400,
            detail="Total salary must be finite"
        )

    average = total_salary / employee_count

    return {"average_salary": average}


# ------------------------------------------------
# ERROR 2: KeyError
# ------------------------------------------------

@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):
    employees = {
        101: {"name": "Rahul", "department": "IT"},
        102: {"name": "Priya", "department": "HR"}
    }
    employee = employees.get(employee_id)
    if employee is None:
        raise HTTPException(
            status_code=404,
            detail=f"Employee {employee_id} not found"
        )
    return employee


@app.get("/")
def home():
    return {"message": "Runtime Debugging Lab"}
