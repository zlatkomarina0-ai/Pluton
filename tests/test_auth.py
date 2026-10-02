import pytest
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import User

client = TestClient(app)


@pytest.fixture
def db():
    """Database fixture for cleanup"""
    yield SessionLocal()


def test_register_success(db):
    """Test successful user registration"""
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "password123",
            "full_name": "New User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data
    assert data["user"]["email"] == "newuser@example.com"
    assert data["user"]["username"] == "newuser"

    # Cleanup
    db.query(User).filter(User.email == "newuser@example.com").delete()
    db.commit()


def test_register_duplicate_email(db):
    """Test registration with duplicate email fails"""
    # Create first user
    client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "password123",
        },
    )

    # Try to create second user with same email
    response = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "user2",
            "password": "password123",
        },
    )
    assert response.status_code == 400

    # Cleanup
    db.query(User).filter(User.email == "duplicate@example.com").delete()
    db.commit()


def test_login_success(db):
    """Test successful login"""
    # Register user
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "password123",
        },
    )

    # Login
    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "login@example.com"

    # Cleanup
    db.query(User).filter(User.email == "login@example.com").delete()
    db.commit()


def test_login_invalid_password(db):
    """Test login with invalid password"""
    # Register user
    client.post(
        "/auth/register",
        json={
            "email": "wrongpass@example.com",
            "username": "wrongpassuser",
            "password": "password123",
        },
    )

    # Try login with wrong password
    response = client.post(
        "/auth/login",
        json={"email": "wrongpass@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401

    # Cleanup
    db.query(User).filter(User.email == "wrongpass@example.com").delete()
    db.commit()


def test_get_current_user(db):
    """Test getting current user with valid token"""
    # Register and login
    register_response = client.post(
        "/auth/register",
        json={
            "email": "current@example.com",
            "username": "currentuser",
            "password": "password123",
        },
    )
    token = register_response.json()["access_token"]

    # Get current user
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "current@example.com"

    # Cleanup
    db.query(User).filter(User.email == "current@example.com").delete()
    db.commit()


def test_get_current_user_without_token():
    """Test getting current user without token fails"""
    response = client.get("/auth/me")
    assert response.status_code == 401
