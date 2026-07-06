from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.deps import get_db
from apps.drivers import services, schemas
from providers.firebase.auth import get_firebase_user_id
from typing import List

router = APIRouter(prefix="/drivers", tags=["drivers"])

@router.get("/get_all_drivers", response_model=List[schemas.Driver])
async def get_all_drivers(
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.get_all_drivers_service(db)

@router.post("/create_driver", response_model=schemas.Driver)
async def create_driver(
    driver_in: schemas.DriverCreate, 
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.create_driver_service(db, driver_in, current_user_uid)

@router.put("/update_driver/{driver_id}", response_model=schemas.Driver)
async def update_driver(
    driver_id: int,
    driver_in: schemas.DriverUpdate,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    driver = services.update_driver_service(db, driver_id, driver_in, current_user_uid)
    if not driver:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    return driver

@router.delete("/delete_driver/{driver_id}")
async def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    result = services.delete_driver_service(db, driver_id, current_user_uid)
    if not result:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    return result
