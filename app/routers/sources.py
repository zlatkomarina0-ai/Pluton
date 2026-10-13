from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import SourceRegistry
from app.services.polling_service import PollingService
from app.services.source_service import (
    create_source,
    delete_source,
    get_source,
    get_sources,
    update_source,
)

router = APIRouter(prefix="/api", tags=["sources"])

ALLOWED_SPORTS = {"football", "basketball", "handball", "formula1"}


class SourceCreate(BaseModel):
    sport_id: Optional[str] = None
    sport: str = "football"
    name: str
    type: str = "api"
    url: str = Field(..., min_length=1)
    api_key_encrypted: Optional[str] = None
    is_active: bool = True
    priority: int = 100
    status: str = "unknown"


class SourceUpdate(BaseModel):
    sport_id: Optional[str] = None
    sport: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None
    api_key_encrypted: Optional[str] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None
    status: Optional[str] = None


class SourcePollRequest(BaseModel):
    sport: str
    source_id: Optional[str] = None


@router.get("/sources")
def list_sources(sport: Optional[str] = None, db: Session = Depends(get_db)):
    return [ {k: v for k, v in source.__dict__.items() if not k.startswith("_sa_")} for source in get_sources(db, sport=sport) ]


@router.get("/sources/{source_id}")
def get_single_source(source_id: str, db: Session = Depends(get_db)):
    source = get_source(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return {k: v for k, v in source.__dict__.items() if not k.startswith("_sa_")}


@router.post("/sources", status_code=status.HTTP_201_CREATED)
def create_source_route(payload: SourceCreate, db: Session = Depends(get_db)):
    if payload.sport not in ALLOWED_SPORTS:
        raise HTTPException(status_code=400, detail="Invalid sport value")
    source = create_source(db, payload.model_dump())
    return {k: v for k, v in source.__dict__.items() if not k.startswith("_sa_")}


@router.patch("/sources/{source_id}")
def update_source_route(source_id: str, payload: SourceUpdate, db: Session = Depends(get_db)):
    source = get_source(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    cleaned = payload.model_dump(exclude_unset=True)
    if "sport" in cleaned and cleaned["sport"] not in ALLOWED_SPORTS:
        raise HTTPException(status_code=400, detail="Invalid sport value")
    source = update_source(db, source, cleaned)
    return {k: v for k, v in source.__dict__.items() if not k.startswith("_sa_")}


@router.delete("/sources/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source_route(source_id: str, db: Session = Depends(get_db)):
    source = get_source(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    delete_source(db, source)
    return None


@router.post("/sources/poll")
def poll_sources(payload: SourcePollRequest, db: Session = Depends(get_db)):
    if payload.sport not in ALLOWED_SPORTS:
        raise HTTPException(status_code=400, detail="Invalid sport value")

    service = PollingService(db)
    return service.poll_sport(payload.sport, payload.source_id)
