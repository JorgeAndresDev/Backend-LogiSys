from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.deps import get_db
from apps.cashless import services, schemas
from providers.firebase.auth import get_firebase_user_id
from typing import List

router = APIRouter(prefix="/cashless", tags=["cashless"])

@router.get("/get_all", response_model=List[schemas.Cashless])
async def get_all(
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.get_all_cashless_service(db)

@router.post("/create", response_model=schemas.Cashless)
async def create(
    cashless_in: schemas.CashlessCreate,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    result = services.create_cashless_service(db, cashless_in, current_user_uid)
    if not result:
        raise HTTPException(status_code=400, detail="El código Cashless ya existe")
    return result

@router.put("/update/{codigo}", response_model=schemas.Cashless)
async def update(
    codigo: int,
    cashless_in: schemas.CashlessUpdate,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    result = services.update_cashless_service(db, codigo, cashless_in, current_user_uid)
    if not result:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return result

@router.delete("/delete/{codigo}")
async def delete(
    codigo: int,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    result = services.delete_cashless_service(db, codigo, current_user_uid)
    if not result:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return result
