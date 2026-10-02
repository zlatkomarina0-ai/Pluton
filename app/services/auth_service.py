from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models import User


class AuthService:
    @staticmethod
    def register(db: Session, email: str, username: str, password: str, full_name: str | None = None) -> User:
        existing = db.query(User).filter((User.email == email) | (User.username == username)).first()
        if existing:
            raise ValueError("User with this email or username already exists")

        user = User(
            email=email,
            username=username,
            full_name=full_name,
            password_hash=hash_password(password),
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        token = create_access_token(str(user.id))
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_active": user.is_active,
            },
        }
