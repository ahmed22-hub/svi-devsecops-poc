from fastapi.testclient import TestClient

from src.main import app, APP_NAME

client = TestClient(app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_version_ok():
    r = client.get("/version")
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == APP_NAME
    assert "version" in data
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0


def test_generate_log_default_info():
    r = client.post("/generate-log")
    assert r.status_code == 200
    data = r.json()
    assert data["service"] == APP_NAME
    assert data["level"] == "info"
    assert "event_id" in data
    assert "ts" in data


def test_generate_log_error_level():
    r = client.post("/generate-log?level=error")
    assert r.status_code == 200
    data = r.json()
    assert data["level"] == "error"
