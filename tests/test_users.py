import pytest
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import User

client = TestClient(app)


@pytest.fixture
def db():
    yield SessionLocal()


def test_get_users():
    """Test getting users list"""
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_user(db):
    """Test creating a user"""
    response = client.post(
        "/api/v1/users",
        json={
            "email": "testuser@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password_hash": None,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["username"] == "testuser"

    # Cleanup
    db.query(User).filter(User.email == "testuser@example.com").delete()
    db.commit()


def test_get_user_by_id(db):
    """Test getting user by ID"""
    # Create user
    create_response = client.post(
        "/api/v1/users",
        json={
            "email": "getuser@example.com",
            "username": "getuser",
            "full_name": "Get User",
            "password_hash": None,
        },
    )
    user_id = create_response.json()["id"]

    # Get user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "getuser@example.com"

    # Cleanup
    db.query(User).filter(User.email == "getuser@example.com").delete()
    db.commit()
