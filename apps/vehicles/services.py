from sqlalchemy.orm import Session
from apps.vehicles.repository import vehicle_repository
from apps.vehicles.schemas import VehicleCreate, VehicleUpdate
from database.models.audit import AuditLog

def get_all_vehicles_service(db: Session):
    return vehicle_repository.get_multi(db)

def create_vehicle_service(db: Session, vehicle_in: VehicleCreate, current_user_uid: str = None):
    vehicle = vehicle_repository.create(db, obj_in=vehicle_in)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="CREATE",
        table_affected="vehicles",
        data_new=vehicle_in.model_dump()
    )
    db.add(audit)
    db.commit()
    
    return vehicle

def update_vehicle_service(db: Session, vehicle_id: int, vehicle_in: VehicleUpdate, current_user_uid: str = None):
    db_obj = vehicle_repository.get(db, id=vehicle_id)
    if not db_obj:
        return None
    
    old_data = {"plate": db_obj.plate}
    vehicle = vehicle_repository.update(db, db_obj=db_obj, obj_in=vehicle_in)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="UPDATE",
        table_affected="vehicles",
        data_old=old_data,
        data_new=vehicle_in.model_dump(exclude_unset=True)
    )
    db.add(audit)
    db.commit()
    
    return vehicle

def delete_vehicle_service(db: Session, vehicle_id: int, current_user_uid: str = None):
    db_obj = vehicle_repository.get(db, id=vehicle_id)
    if not db_obj:
        return None
    
    vehicle = vehicle_repository.remove(db, id=vehicle_id)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="DELETE",
        table_affected="vehicles",
        data_old={"id": vehicle_id, "plate": db_obj.plate}
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Vehículo eliminado correctamente"}
