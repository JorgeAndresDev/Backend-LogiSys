from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class VehicleBase(BaseModel):
    plate: str
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(VehicleBase):
    plate: Optional[str] = None

class VehicleInDBBase(VehicleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Vehicle(VehicleInDBBase):
    pass

class VehicleDocumentSchema(BaseModel):
    document_type: str
    expiration_date: date
    file_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class MaintenanceSchema(BaseModel):
    description: str
    date: date
    model_config = ConfigDict(from_attributes=True)