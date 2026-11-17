from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import database
from database import Base, get_db
from models import Alert


ALERT_PAYLOAD = {
    "title": "CPU spike",
    "severity": "critical",
    "source": "api-gateway",
    "metric_name": "cpu_utilization",
    "metric_value": 96.5,
    "threshold": 85.0,
}


@pytest.fixture
def client(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    test_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    monkeypatch.setattr(database, "engine", engine)

    from main import app

    def override_get_db():
        with test_session() as session:
            yield session

    monkeypatch.setitem(app.dependency_overrides, get_db, override_get_db)
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        engine.dispose()


def test_create_alert(client: TestClient) -> None:
    response = client.post("/alerts/", json=ALERT_PAYLOAD)

    assert response.status_code == 201
    alert = response.json()
    assert isinstance(alert["id"], int)
    assert {key: alert[key] for key in ALERT_PAYLOAD} == ALERT_PAYLOAD
    assert datetime.fromisoformat(alert["created_at"])


def test_list_alerts(client: TestClient) -> None:
    assert client.get("/alerts/").json() == []
    created = client.post("/alerts/", json=ALERT_PAYLOAD)
    assert created.status_code == 201

    response = client.get("/alerts/")

    assert response.status_code == 200
    assert response.json() == [created.json()]


def test_get_alert_by_id(client: TestClient) -> None:
    created = client.post("/alerts/", json=ALERT_PAYLOAD)
    assert created.status_code == 201
    alert = created.json()

    response = client.get(f"/alerts/{alert['id']}")

    assert response.status_code == 200
    assert response.json() == alert


def test_explain_alert(client: TestClient) -> None:
    created = client.post("/alerts/", json=ALERT_PAYLOAD)
    assert created.status_code == 201
    alert = created.json()

    response = client.post(f"/alerts/{alert['id']}/explain")

    assert response.status_code == 200
    explanation = response.json()
    assert explanation["alert_id"] == alert["id"]
    assert alert["severity"] in explanation["explanation"]
    assert alert["metric_name"] in explanation["explanation"]
    assert datetime.fromisoformat(explanation["generated_at"])


def _create_alert(client: TestClient, **overrides: str | float) -> dict:
    payload: dict[str, str | float] = {
        "title": "Test alert",
        "severity": "warning",
        "source": "test-source",
        "metric_name": "test_metric",
        "metric_value": 50.0,
        "threshold": 40.0,
    }
    payload.update(overrides)
    response = client.post("/alerts", json=payload)
    assert response.status_code == 201
    return response.json()


def test_explain_alert_for_nonexistent_id_returns_404(client: TestClient) -> None:
    response = client.post("/alerts/999/explain")

    assert response.status_code == 404
    assert response.json()["detail"] == "Alert not found"


def test_explain_alert_when_metric_is_below_threshold(client: TestClient) -> None:
    alert = _create_alert(
        client,
        title="Connection pool below minimum",
        severity="warning",
        source="db-pool",
        metric_name="active_connections",
        metric_value=2,
        threshold=10,
    )

    response = client.post(f"/alerts/{alert['id']}/explain")

    assert response.status_code == 200
    assert "fell below its threshold" in response.json()["explanation"]


def test_explain_alert_with_zero_threshold_does_not_crash(client: TestClient) -> None:
    alert = _create_alert(
        client,
        title="Unexpected traffic on idle endpoint",
        severity="info",
        source="edge-cache",
        metric_name="request_count",
        metric_value=5,
        threshold=0,
    )

    response = client.post(f"/alerts/{alert['id']}/explain")

    assert response.status_code == 200
    assert "threshold of 0.0" in response.json()["explanation"]