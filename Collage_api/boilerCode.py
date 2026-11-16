from flask import Flask, jsonify

from connection import getSqliteConnection


app = Flask(__name__)


@app.get("/departments")
def departments():
    connection = getSqliteConnection()
    try:
        rows = connection.execute(
            """
            SELECT DepartmentId, DepartmentName
            FROM departments
            ORDER BY DepartmentId
            """
        ).fetchall()
        return jsonify(
            [
                {"DepartmentId": department_id, "DepartmentName": department_name}
                for department_id, department_name in rows
            ]
        )
    finally:
        connection.close()


@app.get("/studentDepartments")
def studentDepartments():
    connection = getSqliteConnection()
    try:
        rows = connection.execute(
            """
            SELECT students.StudentName, departments.DepartmentName
            FROM students
            LEFT JOIN departments
                ON students.DepartmentId = departments.DepartmentId
            ORDER BY students.StudentId
            """
        ).fetchall()
        return jsonify(
            [
                {"studentName": student_name, "departmentName": department_name}
                for student_name, department_name in rows
            ]
        )
    finally:
        connection.close()


if __name__ == "__main__":
    app.run()