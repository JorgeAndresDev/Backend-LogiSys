from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class FirstAidInspectionBase(BaseModel):
    placa_vehiculo: str
    gasas_limpias: Optional[str] = None
    esparadrapo_tela: Optional[str] = None
    baja_lenguas: Optional[str] = None
    guantes_latex: Optional[str] = None
    venda_elastica_2: Optional[str] = None
    venda_elastica_3: Optional[str] = None
    venda_elastica_5: Optional[str] = None
    venda_algodon: Optional[str] = None
    yodopovidona: Optional[str] = None
    solucion_salina: Optional[str] = None
    termometro_digital: Optional[str] = None
    alcohol_antiseptico: Optional[str] = None
    botella_agua: Optional[str] = None
    bandas_adhesivas: Optional[str] = None
    tijeras_punta_roma: Optional[str] = None
    pito_emergencias: Optional[str] = None
    manual_primeros_auxilios: Optional[str] = None
    observaciones: Optional[str] = None

class FirstAidInspectionCreate(FirstAidInspectionBase):
    pass

class FirstAidInspectionUpdate(FirstAidInspectionBase):
    placa_vehiculo: Optional[str] = None
    gasas_limpias: Optional[str] = None
    esparadrapo_tela: Optional[str] = None
    baja_lenguas: Optional[str] = None
    guantes_latex: Optional[str] = None
    venda_elastica_2: Optional[str] = None
    venda_elastica_3: Optional[str] = None
    venda_elastica_5: Optional[str] = None
    venda_algodon: Optional[str] = None
    yodopovidona: Optional[str] = None
    solucion_salina: Optional[str] = None
    termometro_digital: Optional[str] = None
    alcohol_antiseptico: Optional[str] = None
    botella_agua: Optional[str] = None
    bandas_adhesivas: Optional[str] = None
    tijeras_punta_roma: Optional[str] = None
    pito_emergencias: Optional[str] = None
    manual_primeros_auxilios: Optional[str] = None

class FirstAidInspectionInDBBase(FirstAidInspectionBase):
    id: int
    fecha_inspeccion: datetime
    model_config = ConfigDict(from_attributes=True)

class FirstAidInspection(FirstAidInspectionInDBBase):
    pass
