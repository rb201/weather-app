from fastapi.testclient import TestClient

from backend.api import app

client = TestClient(app)


def test_health_check_endpoint():
    res = client.get("/health")

    assert res.status_code == 200
    assert res.json() == {"service": "ok"}


def test_health_check_method():
    res = client.post("/health")

    assert res.status_code == 405
