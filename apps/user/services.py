from sqlalchemy.orm import Session
from sqlalchemy import func
from apps.user.repository import user_repository
from apps.user.schemas import UserCreate, UserUpdate
from database.models.user import User, Role, AllowedEmail

from database.models.audit import AuditLog
from typing import List, Optional

def get_all_users_service(db: Session):
    return user_repository.get_multi(db)

def create_user_service(db: Session, user_in: UserCreate, current_user_uid: str = None):
    user = user_repository.create(db, obj_in=user_in)
    
    # Asignar rol 'user' por defecto
    user_repository.assign_role(db, user_id=user.id, role_name="user")
    
    audit = AuditLog(
        user_id=current_user_uid,
        action="CREATE",
        table_affected="users",
        data_new=user_in.model_dump()
    )
    db.add(audit)
    db.commit()
    
    return user

def update_user_service(db: Session, user_id: int, user_in: UserUpdate, current_user_uid: str = None):
    db_obj = user_repository.get(db, id=user_id)
    if not db_obj:
        return None
    
    old_data = {"email": db_obj.email, "full_name": db_obj.full_name}
    user = user_repository.update(db, db_obj=db_obj, obj_in=user_in)
    
    audit = AuditLog(
        user_id=current_user_uid,
        action="UPDATE",
        table_affected="users",
        data_old=old_data,
        data_new=user_in.model_dump(exclude_unset=True)
    )
    db.add(audit)
    db.commit()
    
    return user

def delete_user_service(db: Session, user_id: int, current_user_uid: str = None):
    db_obj = user_repository.get(db, id=user_id)
    if not db_obj:
        return None
    
    user = user_repository.remove(db, id=user_id)
    
    audit = AuditLog(
        user_id=current_user_uid,
        action="DELETE",
        table_affected="users",
        data_old={"id": user_id, "email": db_obj.email}
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Usuario eliminado correctamente"}

def get_all_roles_service(db: Session):
    return user_repository.get_all_roles(db)

def assign_role_service(db: Session, user_id: int, role_name: str, current_user_uid: str = None):
    user = user_repository.assign_role(db, user_id=user_id, role_name=role_name)
    if user:
        audit = AuditLog(
            user_id=current_user_uid,
            action="UPDATE",
            table_affected="user_roles",
            data_new={"user_id": user_id, "role_assigned": role_name}
        )
        db.add(audit)
        db.commit()
    return user

def remove_role_service(db: Session, user_id: int, role_name: str, current_user_uid: str = None):
    user = user_repository.remove_role(db, user_id=user_id, role_name=role_name)
    if user:
        audit = AuditLog(
            user_id=current_user_uid,
            action="UPDATE",
            table_affected="user_roles",
            data_new={"user_id": user_id, "role_removed": role_name}
        )
        db.add(audit)
        db.commit()
    return user

def get_allowed_emails_service(db: Session):
    return user_repository.get_allowed_emails(db)

def add_allowed_email_service(db: Session, email: str, current_user_uid: str = None):
    # Obtener el user_id desde el firebase_uid
    user = user_repository.get_by_firebase_uid(db, uid=current_user_uid)
    created_by = user.id if user else None
    entry = user_repository.add_allowed_email(db, email=email, created_by=created_by)
    
    # Pre-crear un registro de usuario para que aparezca en la lista de usuarios
    existing_user = user_repository.get_by_email(db, email=email)
    if not existing_user:
        user_in = UserCreate(email=email, full_name=email.split('@')[0], is_active=True)
        new_user = user_repository.create(db, obj_in=user_in)
        user_repository.assign_role(db, user_id=new_user.id, role_name="user")
    
    audit = AuditLog(
        user_id=current_user_uid,
        action="CREATE",
        table_affected="allowed_emails",
        data_new={"email": email}
    )
    db.add(audit)
    db.commit()
    
    return entry

def delete_allowed_email_service(db: Session, entry_id: int):
    entry = user_repository.remove_allowed_email(db, entry_id=entry_id)
    return entry

def toggle_user_active_service(db: Session, user_id: int, current_user_uid: str = None):
    db_obj = user_repository.get(db, id=user_id)
    if not db_obj:
        return None
    db_obj.is_active = not db_obj.is_active
    audit = AuditLog(
        user_id=current_user_uid,
        action="UPDATE",
        table_affected="users",
        data_new={"is_active": db_obj.is_active}
    )
    db.add(audit)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_user_stats_service(db: Session):
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    admin_users = len(admin_role.users) if admin_role else 0
    whitelist_count = db.query(AllowedEmail).count()
    return {
        "total_users": total_users,
        "active_users": active_users,
        "admin_users": admin_users,
        "whitelist_count": whitelist_count,
    }

def get_connection_history_service(db: Session):
    users = db.query(User).order_by(User.last_login.desc().nullslast()).all()
    return [
        {
            "user_id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "last_login": u.last_login.isoformat() if u.last_login else None,
        }
        for u in users
    ]
