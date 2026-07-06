from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.deps import get_db
from apps.audit import services, schemas
from providers.firebase.auth import get_firebase_user_id
from typing import List

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("/get_all", response_model=List[schemas.AuditLog])
async def get_all_logs(
    db: Session = Depends(get_db),
    limit: int = 100,
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.get_all_audit_logs_service(db, limit)
