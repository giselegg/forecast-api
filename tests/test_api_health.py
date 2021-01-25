from datetime import datetime
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health():
    response = client.get("/health/")
    assert response.status_code == 200

    try:
        assert datetime.fromisoformat(response.json().get("timestamp"))
    except ValueError:
        assert False
