from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

# Basic Schemas
class DriverBase(BaseModel):
    cedula: str
    name: str
    phone: Optional[str] = None

class DriverCreate(DriverBase):
    pass

class DriverUpdate(DriverBase):
    cedula: Optional[str] = None
    name: Optional[str] = None

class DriverInDBBase(DriverBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Driver(DriverInDBBase):
    pass

# Nested Data Schemas
class LicenseSchema(BaseModel):
    category: str
    expiration_date: date
    model_config = ConfigDict(from_attributes=True)

class DriverWithDetails(Driver):
    licenses: List[LicenseSchema] = []