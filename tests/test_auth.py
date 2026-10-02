import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import SessionLocal
from app.models import User

client = TestClient(app)


@pytest.fixture
def db():
    """Database fixture"""
    db = SessionLocal()
    yield db
    db.close()


def test_register_success(db: Session):
    """Test successful user registration"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert data["user"]["email"] == "test@example.com"
    
    # Cleanup
    db.query(User).filter(User.email == "test@example.com").delete()
    db.commit()


def test_register_duplicate_email(db: Session):
    """Test registration with duplicate email"""
    client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "password123",
        },
    )
    
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


def test_login_success(db: Session):
    """Test successful login"""
    # Register first
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
    assert data["access_token"]
    assert data["user"]["email"] == "login@example.com"
    
    # Cleanup
    db.query(User).filter(User.email == "login@example.com").delete()
    db.commit()


def test_login_invalid_password(db: Session):
    """Test login with invalid password"""
    # Register first
    client.post(
        "/auth/register",
        json={
            "email": "invalid@example.com",
            "username": "invaliduser",
            "password": "password123",
        },
    )
    
    # Login with wrong password
    response = client.post(
        "/auth/login",
        json={"email": "invalid@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    
    # Cleanup
    db.query(User).filter(User.email == "invalid@example.com").delete()
    db.commit()


def test_get_me_with_token(db: Session):
    """Test getting current user with valid token"""
    # Register and get token
    register_response = client.post(
        "/auth/register",
        json={
            "email": "getme@example.com",
            "username": "getmeuser",
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
    assert data["email"] == "getme@example.com"
    
    # Cleanup
    db.query(User).filter(User.email == "getme@example.com").delete()
    db.commit()


def test_get_me_without_token():
    """Test getting current user without token"""
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_get_me_with_invalid_token():
    """Test getting current user with invalid token"""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
