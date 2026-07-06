from pydantic import BaseModel, ConfigDict
from typing import Optional

class EmployeeBase(BaseModel):
    cc: str
    name: str
    cargo: Optional[str] = None
    area: Optional[str] = None
    phone: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    cc: Optional[str] = None
    name: Optional[str] = None
    cargo: Optional[str] = None
    area: Optional[str] = None
    phone: Optional[str] = None

class Employee(EmployeeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
