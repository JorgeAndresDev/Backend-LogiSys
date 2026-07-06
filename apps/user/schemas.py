from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    firebase_uid: Optional[str] = None

class UserUpdate(UserBase):
    full_name: Optional[str] = None
    email: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    firebase_uid: Optional[str] = None
    last_login: Optional[str] = None
    roles: List[str] = []

    model_config = ConfigDict(from_attributes=True)

    @field_validator('roles', mode='before')
    @classmethod
    def coerce_roles(cls, v):
        if isinstance(v, list):
            return [r.name if hasattr(r, 'name') else str(r) for r in v]
        return v

    @field_validator('last_login', mode='before')
    @classmethod
    def coerce_last_login(cls, v):
        if v is None:
            return None
        if hasattr(v, 'isoformat'):
            return v.isoformat()
        return str(v)

class User(UserInDBBase):
    pass

class UserStats(BaseModel):
    total_users: int
    active_users: int
    admin_users: int
    whitelist_count: int

class ConnectionLog(BaseModel):
    user_id: int
    email: str
    full_name: Optional[str] = None
    last_login: Optional[str] = None

class RoleSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class AssignRoleRequest(BaseModel):
    user_id: int
    role_name: str

class AllowedEmailCreate(BaseModel):
    email: str

class AllowedEmailResponse(BaseModel):
    id: int
    email: str
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
