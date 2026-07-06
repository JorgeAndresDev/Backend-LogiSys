from sqlalchemy.orm import Session
from apps.cashless.repository import cashless_repository
from apps.cashless.schemas import CashlessCreate, CashlessUpdate
from database.models.audit import AuditLog
from typing import List

def get_all_cashless_service(db: Session):
    return cashless_repository.get_multi(db)

def create_cashless_service(db: Session, cashless_in: CashlessCreate, current_user_uid: str = None):
    # Verify if code already exists
    existing = cashless_repository.get_by_codigo(db, codigo=cashless_in.codigo)
    if existing:
        return None
        
    created_obj = cashless_repository.create(db, obj_in=cashless_in)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="CREATE",
        table_affected="tbl_cashless",
        data_new=cashless_in.model_dump()
    )
    db.add(audit)
    db.commit()
    
    return created_obj

def update_cashless_service(db: Session, codigo: int, cashless_in: CashlessUpdate, current_user_uid: str = None):
    db_obj = cashless_repository.get_by_codigo(db, codigo=codigo)
    if not db_obj:
        return None
    
    old_data = {"novedad": db_obj.novedad}
    updated_obj = cashless_repository.update(db, db_obj=db_obj, obj_in=cashless_in)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="UPDATE",
        table_affected="tbl_cashless",
        data_old=old_data,
        data_new=cashless_in.model_dump()
    )
    db.add(audit)
    db.commit()
    
    return updated_obj

def delete_cashless_service(db: Session, codigo: int, current_user_uid: str = None):
    db_obj = cashless_repository.get_by_codigo(db, codigo=codigo)
    if not db_obj:
        return None
    
    cashless_repository.remove(db, id=codigo)
    
    # Audit Log
    audit = AuditLog(
        user_id=current_user_uid,
        action="DELETE",
        table_affected="tbl_cashless",
        data_old={"codigo": codigo, "cliente": db_obj.cliente}
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Registro eliminado correctamente"}
