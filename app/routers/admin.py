from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.audit_service import AuditService
from app.services.source_service import delete_source, get_source

router = APIRouter(prefix="/api/admin", tags=["admin"])


class DeleteApprovalRequest(BaseModel):
    approved: bool = False
    reason: str = "manual_delete"
    user_id: str | None = None


@router.post("/approve-delete")
def approve_delete(entity_type: str, entity_id: str, payload: DeleteApprovalRequest, db: Session = Depends(get_db)):
    if not payload.approved:
        raise HTTPException(status_code=400, detail="Delete approval is required before destructive action.")

    AuditService.log_delete(
        db,
        entity_type=entity_type,
        entity_id=entity_id,
        user_id=payload.user_id,
        reason=payload.reason,
    )

    return {"status": "approved", "entity_type": entity_type, "entity_id": entity_id}
