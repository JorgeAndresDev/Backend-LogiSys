from pydantic import BaseModel, ConfigDict
from typing import Optional

class CashlessBase(BaseModel):
    cliente: str
    dt: int
    placa: str
    numero: int
    novedad: Optional[str] = None

class CashlessCreate(CashlessBase):
    codigo: int

class CashlessUpdate(BaseModel):
    novedad: str

class CashlessInDBBase(CashlessBase):
    codigo: int
    model_config = ConfigDict(from_attributes=True)

class Cashless(CashlessInDBBase):
    pass
