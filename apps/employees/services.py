from sqlalchemy.orm import Session
from apps.employees.repository import employee_repository
from apps.employees.schemas import EmployeeCreate, EmployeeUpdate
from database.models.audit import AuditLog

def get_all_employees_service(db: Session):
    return employee_repository.get_multi(db)

def get_employee_by_cc_service(db: Session, cc: str):
    return employee_repository.get_by_cc(db, cc=cc)

def create_employee_service(db: Session, employee_in: EmployeeCreate, current_user_uid: str = None):
    # Verificar si ya existe
    if employee_repository.get_by_cc(db, cc=employee_in.cc):
        return None
    
    employee = employee_repository.create(db, obj_in=employee_in)
    
    # Auditoria
    audit = AuditLog(
        user_id=current_user_uid,
        action="CREATE",
        table_affected="employees",
        data_new=employee_in.model_dump()
    )
    db.add(audit)
    db.commit()
    
    return employee

def update_employee_service(db: Session, cc: str, employee_in: EmployeeUpdate, current_user_uid: str = None):
    db_obj = employee_repository.get_by_cc(db, cc=cc)
    if not db_obj:
        return None
    
    old_data = {"name": db_obj.name, "cargo": db_obj.cargo}
    updated_obj = employee_repository.update(db, db_obj=db_obj, obj_in=employee_in)
    
    # Auditoria
    audit = AuditLog(
        user_id=current_user_uid,
        action="UPDATE",
        table_affected="employees",
        data_old=old_data,
        data_new=employee_in.model_dump(exclude_unset=True)
    )
    db.add(audit)
    db.commit()
    
    return updated_obj

def delete_employee_service(db: Session, cc: str, current_user_uid: str = None):
    db_obj = employee_repository.get_by_cc(db, cc=cc)
    if not db_obj:
        return None
    
    employee_repository.remove(db, id=db_obj.id)
    
    # Auditoria
    audit = AuditLog(
        user_id=current_user_uid,
        action="DELETE",
        table_affected="employees",
        data_old={"cc": cc, "name": db_obj.name}
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Empleado eliminado correctamente"}
