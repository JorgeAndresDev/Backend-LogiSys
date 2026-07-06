from sqlalchemy.orm import Session
from apps.drivers.repository import driver_repository
from apps.drivers.schemas import DriverCreate, DriverUpdate
from database.models.audit import AuditLog

def get_all_drivers_service(db: Session):
    return driver_repository.get_multi(db)

def create_driver_service(db: Session, driver_in: DriverCreate, current_user_uid: str = None):
    driver = driver_repository.create(db, obj_in=driver_in)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="CREATE",
        table_affected="drivers",
        data_new=driver_in.model_dump()
    )
    db.add(audit)
    db.commit()
    
    return driver

def update_driver_service(db: Session, driver_id: int, driver_in: DriverUpdate, current_user_uid: str = None):
    db_obj = driver_repository.get(db, id=driver_id)
    if not db_obj:
        return None
    
    old_data = {"cedula": db_obj.cedula, "name": db_obj.name}
    driver = driver_repository.update(db, db_obj=db_obj, obj_in=driver_in)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="UPDATE",
        table_affected="drivers",
        data_old=old_data,
        data_new=driver_in.model_dump(exclude_unset=True)
    )
    db.add(audit)
    db.commit()
    
    return driver

def delete_driver_service(db: Session, driver_id: int, current_user_uid: str = None):
    db_obj = driver_repository.get(db, id=driver_id)
    if not db_obj:
        return None
    
    driver = driver_repository.remove(db, id=driver_id)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="DELETE",
        table_affected="drivers",
        data_old={"id": driver_id, "cedula": db_obj.cedula}
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Conductor eliminado correctamente"}
