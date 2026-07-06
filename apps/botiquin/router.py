from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.deps import get_db
from apps.botiquin import services, schemas
from providers.firebase.auth import get_firebase_user_id
from typing import List

router = APIRouter(prefix="/botiquin", tags=["botiquin"])

@router.get("/get_all_inspections", response_model=List[schemas.FirstAidInspection])
async def get_all_inspections(
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.get_all_first_aid_inspections_service(db)

@router.get("/get_detail/{inspection_id}", response_model=schemas.FirstAidInspection)
async def get_detail(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    inspection = services.get_first_aid_inspection_detail_service(db, inspection_id)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspección no encontrada")
    return inspection

@router.post("/create_inspection", response_model=schemas.FirstAidInspection)
async def create_inspection(
    inspection_in: schemas.FirstAidInspectionCreate, 
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.create_first_aid_inspection_service(db, inspection_in, current_user_uid)

@router.put("/update_inspection/{inspection_id}", response_model=schemas.FirstAidInspection)
async def update_inspection(
    inspection_id: int,
    inspection_in: schemas.FirstAidInspectionUpdate,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    inspection = services.update_first_aid_inspection_service(db, inspection_id, inspection_in, current_user_uid)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspección no encontrada")
    return inspection

@router.delete("/delete_inspection/{inspection_id}")
async def delete_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    result = services.delete_first_aid_inspection_service(db, inspection_id, current_user_uid)
    if not result:
        raise HTTPException(status_code=404, detail="Inspección no encontrada")
    return result
