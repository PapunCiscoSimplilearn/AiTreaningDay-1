import pytest
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


@pytest.mark.parametrize(
    ("path", "status_code", "body"),
    [
        ("/employee/bonus", 200, {"bonus": 5000.0}),
        ("/employee/average-salary", 200, {"average_salary": 50000.0}),
        ("/employee/average-salary?employee_count=0", 400, {"detail": "Employee count must be greater than zero"}),
        ("/employee/average-salary?employee_count=-1", 400, {"detail": "Employee count must be greater than zero"}),
        ("/employee/average-salary?total_salary=nan", 400, {"detail": "Total salary must be finite"}),
        ("/employee/average-salary?total_salary=inf", 400, {"detail": "Total salary must be finite"}),
        ("/employee/average-salary?total_salary=-inf", 400, {"detail": "Total salary must be finite"}),
        ("/employee/101", 200, {"name": "Rahul", "department": "IT"}),
        ("/employee/999", 404, {"detail": "Employee 999 not found"}),
    ],
)
def test_employee_endpoints(path, status_code, body):
    response = client.get(path)

    assert response.status_code == status_code
    assert response.json() == body