from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "PLUTON"}
