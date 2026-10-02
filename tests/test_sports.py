import pytest
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import Sport

client = TestClient(app)


@pytest.fixture
def db():
    yield SessionLocal()


def test_get_sports():
    """Test getting sports list"""
    response = client.get("/api/v1/sports")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_sport(db):
    """Test creating a sport"""
    response = client.post(
        "/api/v1/sports",
        json={
            "code": "TEST_SPORT",
            "name": "Test Sport",
            "active": True,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "TEST_SPORT"
    assert data["name"] == "Test Sport"
    assert data["active"] is True
    assert "id" in data

    # Cleanup
    db.query(Sport).filter(Sport.code == "TEST_SPORT").delete()
    db.commit()


def test_create_duplicate_sport_code(db):
    """Test creating sport with duplicate code fails"""
    # Create first sport
    client.post(
        "/api/v1/sports",
        json={
            "code": "DUP_CODE",
            "name": "First Sport",
            "active": True,
        },
    )

    # Try to create second sport with same code
    response = client.post(
        "/api/v1/sports",
        json={
            "code": "DUP_CODE",
            "name": "Second Sport",
            "active": True,
        },
    )
    assert response.status_code == 400

    # Cleanup
    db.query(Sport).filter(Sport.code == "DUP_CODE").delete()
    db.commit()


def test_get_sport_by_id(db):
    """Test getting sport by ID"""
    # Create sport
    create_response = client.post(
        "/api/v1/sports",
        json={
            "code": "GET_TEST",
            "name": "Get Test Sport",
            "active": True,
        },
    )
    sport_id = create_response.json()["id"]

    # Get sport
    response = client.get(f"/api/v1/sports/{sport_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sport_id
    assert data["code"] == "GET_TEST"

    # Cleanup
    db.query(Sport).filter(Sport.code == "GET_TEST").delete()
    db.commit()


def test_get_nonexistent_sport():
    """Test getting nonexistent sport returns 404"""
    response = client.get("/api/v1/sports/nonexistent-id")
    assert response.status_code == 404
