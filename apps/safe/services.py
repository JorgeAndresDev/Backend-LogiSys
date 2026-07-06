from sqlalchemy.orm import Session
from apps.safe.repository import safe_inspection_repository
from apps.safe.schemas import SafeInspectionCreate, SafeInspectionUpdate
from database.models.audit import AuditLog

def create_safe_inspection_service(db: Session, inspection_in: SafeInspectionCreate, current_user_uid: str = None):
    inspection = safe_inspection_repository.create(db, obj_in=inspection_in)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="CREATE",
        table_affected="inspeccion_cajas_fuertes",
        data_new=inspection_in.model_dump()
    )
    db.add(audit)
    db.commit()
    
    return inspection

def get_all_safe_inspections_service(db: Session):
    return safe_inspection_repository.get_multi(db)

def get_safe_inspection_detail_service(db: Session, inspection_id: int):
    return safe_inspection_repository.get(db, id=inspection_id)

def update_safe_inspection_service(db: Session, inspection_id: int, inspection_in: SafeInspectionUpdate, current_user_uid: str = None):
    db_obj = safe_inspection_repository.get(db, id=inspection_id)
    if not db_obj:
        return None
    
    inspection = safe_inspection_repository.update(db, db_obj=db_obj, obj_in=inspection_in)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="UPDATE",
        table_affected="inspeccion_cajas_fuertes",
        data_new=inspection_in.model_dump(exclude_unset=True)
    )
    db.add(audit)
    db.commit()
    
    return inspection

def delete_safe_inspection_service(db: Session, inspection_id: int, current_user_uid: str = None):
    db_obj = safe_inspection_repository.get(db, id=inspection_id)
    if not db_obj:
        return None
    
    safe_inspection_repository.remove(db, id=inspection_id)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="DELETE",
        table_affected="inspeccion_cajas_fuertes",
        data_old={"id": inspection_id, "placa": db_obj.placa_vehiculo}
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Inspección eliminada correctamente"}
