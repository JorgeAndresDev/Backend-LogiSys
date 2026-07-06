from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class SafeInspectionBase(BaseModel):
    placa_vehiculo: str
    puerta_estado: str
    puerta_facilidad: str
    clave_precisa: str
    clave_autorizada: str
    perilla_funciona: str
    numeros_visibles: str
    caja_anclada: str
    observaciones: Optional[str] = None

class SafeInspectionCreate(SafeInspectionBase):
    pass

class SafeInspectionUpdate(SafeInspectionBase):
    placa_vehiculo: Optional[str] = None
    puerta_estado: Optional[str] = None
    puerta_facilidad: Optional[str] = None
    clave_precisa: Optional[str] = None
    clave_autorizada: Optional[str] = None
    perilla_funciona: Optional[str] = None
    numeros_visibles: Optional[str] = None
    caja_anclada: Optional[str] = None

class SafeInspectionInDBBase(SafeInspectionBase):
    id: int
    fecha_inspeccion: datetime
    model_config = ConfigDict(from_attributes=True)

class SafeInspection(SafeInspectionInDBBase):
    pass
