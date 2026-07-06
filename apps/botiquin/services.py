from sqlalchemy.orm import Session
from apps.botiquin.repository import first_aid_repository
from apps.botiquin.schemas import FirstAidInspectionCreate, FirstAidInspectionUpdate
from database.models.audit import AuditLog

def create_first_aid_inspection_service(db: Session, inspection_in: FirstAidInspectionCreate, current_user_uid: str = None):
    inspection = first_aid_repository.create(db, obj_in=inspection_in)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="CREATE",
        table_affected="inspecciones_botiquines",
        data_new=inspection_in.model_dump()
    )
    db.add(audit)
    db.commit()
    
    return inspection

def get_all_first_aid_inspections_service(db: Session):
    return first_aid_repository.get_multi(db)

def get_first_aid_inspection_detail_service(db: Session, inspection_id: int):
    return first_aid_repository.get(db, id=inspection_id)

def update_first_aid_inspection_service(db: Session, inspection_id: int, inspection_in: FirstAidInspectionUpdate, current_user_uid: str = None):
    db_obj = first_aid_repository.get(db, id=inspection_id)
    if not db_obj:
        return None
    
    inspection = first_aid_repository.update(db, db_obj=db_obj, obj_in=inspection_in)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="UPDATE",
        table_affected="inspecciones_botiquines",
        data_new=inspection_in.model_dump(exclude_unset=True)
    )
    db.add(audit)
    db.commit()
    
    return inspection

def delete_first_aid_inspection_service(db: Session, inspection_id: int, current_user_uid: str = None):
    db_obj = first_aid_repository.get(db, id=inspection_id)
    if not db_obj:
        return None
    
    first_aid_repository.remove(db, id=inspection_id)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="DELETE",
        table_affected="inspecciones_botiquines",
        data_old={"id": inspection_id, "placa": db_obj.placa_vehiculo}
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Inspección de botiquín eliminada correctamente"}
