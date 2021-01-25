from datetime import datetime
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health() -> None:
    """
    Checks if health returns timestamp
    """
    response = client.get("/health/")
    assert response.status_code == 200

    try:
        assert datetime.fromisoformat(response.json().get("timestamp"))
    except ValueError:
        assert False


def test_fail_get_forecast():
    response = client.get("/forecast")
    assert response.status_code == 404


def test_assert_get_forecast():
    response = client.get("forecast/palhoça")
    assert response.status_code == 200
