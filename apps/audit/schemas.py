from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class AuditLogBase(BaseModel):
    user_id: Optional[str] = None
    action: str
    table_affected: str
    data_old: Optional[Dict[str, Any]] = None
    data_new: Optional[Dict[str, Any]] = None

class AuditLog(AuditLogBase):
    id: int
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)
