from firebase_admin import auth as firebase_auth
from jose import jwt, JWTError

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import settings
from sqlalchemy.orm import Session
from database.deps import get_db
from database.models.user import User

security = HTTPBearer()

async def verify_internal_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido o expirado: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_firebase_user_id(token_data: dict = Depends(verify_internal_token)) -> str:
    return token_data.get("uid")

def require_admin(
    token_data: dict = Depends(verify_internal_token),
    db: Session = Depends(get_db)
) -> str:
    uid = token_data.get("uid")
    user = db.query(User).filter(User.firebase_uid == uid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    if not any(role.name == "admin" for role in user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return uid
