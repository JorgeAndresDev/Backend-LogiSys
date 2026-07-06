from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.deps import get_db
from apps.user import services, schemas
from providers.firebase.auth import get_firebase_user_id, require_admin
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/stats", response_model=schemas.UserStats)
async def get_user_stats(
    db: Session = Depends(get_db),
    _: str = Depends(require_admin)
):
    return services.get_user_stats_service(db)

@router.get("/connection-history", response_model=List[schemas.ConnectionLog])
async def get_connection_history(
    db: Session = Depends(get_db),
    _: str = Depends(require_admin)
):
    return services.get_connection_history_service(db)


@router.get("/get_all_users", response_model=List[schemas.User])
async def get_all_users(
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.get_all_users_service(db)

@router.post("/create_user", response_model=schemas.User)
async def create_user(
    user_in: schemas.UserCreate, 
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(require_admin)
):
    return services.create_user_service(db, user_in, current_user_uid)

@router.put("/update_user/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(require_admin)
):
    user = services.update_user_service(db, user_id, user_in, current_user_uid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.delete("/delete_user/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(require_admin)
):
    result = services.delete_user_service(db, user_id, current_user_uid)
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return result

@router.patch("/toggle-active/{user_id}", response_model=schemas.User)
async def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(require_admin)
):
    user = services.toggle_user_active_service(db, user_id, current_user_uid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# --- Role endpoints ---

@router.get("/roles", response_model=List[schemas.RoleSchema])
async def get_all_roles(
    db: Session = Depends(get_db),
    _: str = Depends(require_admin)
):
    return services.get_all_roles_service(db)

@router.post("/assign-role", response_model=schemas.User)
async def assign_role(
    request: schemas.AssignRoleRequest,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(require_admin)
):
    user = services.assign_role_service(db, request.user_id, request.role_name, current_user_uid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario o rol no encontrado")
    return user

@router.post("/remove-role", response_model=schemas.User)
async def remove_role(
    request: schemas.AssignRoleRequest,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(require_admin)
):
    user = services.remove_role_service(db, request.user_id, request.role_name, current_user_uid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# --- Allowed Email endpoints ---

@router.get("/allowed-emails", response_model=List[schemas.AllowedEmailResponse])
async def get_allowed_emails(
    db: Session = Depends(get_db),
    _: str = Depends(require_admin)
):
    return services.get_allowed_emails_service(db)

@router.post("/allowed-emails", response_model=schemas.AllowedEmailResponse)
async def add_allowed_email(
    request: schemas.AllowedEmailCreate,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.add_allowed_email_service(db, request.email, current_user_uid)

@router.delete("/allowed-emails/{entry_id}")
async def delete_allowed_email(
    entry_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_admin)
):
    result = services.delete_allowed_email_service(db, entry_id)
    if not result:
        raise HTTPException(status_code=404, detail="Email no encontrado en whitelist")
    return {"success": True, "message": "Email eliminado de la whitelist"}
