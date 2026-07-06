from database.repository.base import BaseRepository
from database.models.employee import Employee
from apps.employees.schemas import EmployeeCreate, EmployeeUpdate
from sqlalchemy.orm import Session
from typing import Optional

class EmployeeRepository(BaseRepository[Employee, EmployeeCreate, EmployeeUpdate]):
    def get_by_cc(self, db: Session, cc: str) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.cc == cc).first()

employee_repository = EmployeeRepository(Employee)
