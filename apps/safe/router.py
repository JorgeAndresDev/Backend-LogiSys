from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.deps import get_db
from apps.safe import services, schemas
from providers.firebase.auth import get_firebase_user_id
from typing import List

router = APIRouter(prefix="/safe", tags=["safe"])

@router.get("/get_all_inspections", response_model=List[schemas.SafeInspection])
async def get_all_inspections(
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.get_all_safe_inspections_service(db)

@router.get("/get_detail/{inspection_id}", response_model=schemas.SafeInspection)
async def get_detail(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    inspection = services.get_safe_inspection_detail_service(db, inspection_id)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspección no encontrada")
    return inspection

@router.post("/create_inspection", response_model=schemas.SafeInspection)
async def create_inspection(
    inspection_in: schemas.SafeInspectionCreate, 
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.create_safe_inspection_service(db, inspection_in, current_user_uid)

@router.put("/update_inspection/{inspection_id}", response_model=schemas.SafeInspection)
async def update_inspection(
    inspection_id: int,
    inspection_in: schemas.SafeInspectionUpdate,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    inspection = services.update_safe_inspection_service(db, inspection_id, inspection_in, current_user_uid)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspección no encontrada")
    return inspection

@router.delete("/delete_inspection/{inspection_id}")
async def delete_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    result = services.delete_safe_inspection_service(db, inspection_id, current_user_uid)
    if not result:
        raise HTTPException(status_code=404, detail="Inspección no encontrada")
    return result
