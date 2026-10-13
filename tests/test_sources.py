from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_route():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_source_and_list():
    payload = {
        "sport": "football",
        "name": "Example source",
        "type": "api",
        "url": "https://httpbin.org/get",
        "priority": 1,
        "status": "unknown",
    }
    response = client.post("/api/sources", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Example source"

    list_resp = client.get("/api/sources")
    assert list_resp.status_code == 200
    assert any(item["name"] == "Example source" for item in list_resp.json())


def test_invalid_sport_is_rejected():
    payload = {
        "sport": "invalidsport",
        "name": "Bad source",
        "type": "api",
        "url": "https://example.com/api",
    }
    response = client.post("/api/sources", json=payload)
    assert response.status_code == 400
