from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.deps import get_db
from apps.employees import services, schemas
from providers.firebase.auth import get_firebase_user_id
from typing import List

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("/get_all_employees", response_model=List[schemas.Employee])
async def get_all_employees(
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    return services.get_all_employees_service(db)

@router.get("/get_employee/{cc}", response_model=schemas.Employee)
async def get_employee(
    cc: str,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    employee = services.get_employee_by_cc_service(db, cc)
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return employee

@router.post("/create_employee", response_model=schemas.Employee)
async def create_employee(
    employee_in: schemas.EmployeeCreate, 
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    employee = services.create_employee_service(db, employee_in, current_user_uid)
    if not employee:
        raise HTTPException(status_code=400, detail="El empleado ya existe o hay un error en los datos")
    return employee

@router.put("/update_employee/{cc}", response_model=schemas.Employee)
async def update_employee(
    cc: str,
    employee_in: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    employee = services.update_employee_service(db, cc, employee_in, current_user_uid)
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return employee

@router.delete("/delete_employee/{cc}")
async def delete_employee(
    cc: str,
    db: Session = Depends(get_db),
    current_user_uid: str = Depends(get_firebase_user_id)
):
    result = services.delete_employee_service(db, cc, current_user_uid)
    if not result:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return result
