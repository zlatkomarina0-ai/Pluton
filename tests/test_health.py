from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "PLUTON"


def test_readiness_check():
    """Test readiness check endpoint"""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["ready"] is True


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["service"] == "PLUTON"
