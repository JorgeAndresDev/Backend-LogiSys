from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.deps import get_db
from apps.vehicles import services, schemas
from providers.firebase.auth import get_firebase_user_id
from typing import List

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.get("/get_all_vehicles", response_model=List[schemas.Vehicle])
async def get_all_vehicles(
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.get_all_vehicles_service(db)

@router.post("/create_vehicle", response_model=schemas.Vehicle)
async def create_vehicle(
    vehicle_in: schemas.VehicleCreate, 
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.create_vehicle_service(db, vehicle_in, current_user_uid)

@router.put("/update_vehicle/{vehicle_id}", response_model=schemas.Vehicle)
async def update_vehicle(
    vehicle_id: int,
    vehicle_in: schemas.VehicleUpdate,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    vehicle = services.update_vehicle_service(db, vehicle_id, vehicle_in, current_user_uid)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehicle

@router.delete("/delete_vehicle/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    result = services.delete_vehicle_service(db, vehicle_id, current_user_uid)
    if not result:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return result
