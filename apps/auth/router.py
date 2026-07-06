from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from database.deps import get_db
from apps.auth import services
from pydantic import BaseModel
from core.limiter import limiter

auth = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    firebase_token: str

@auth.post("/login")
@limiter.limit("10/minute")
async def login(request: Request, body: LoginRequest, db: Session = Depends(get_db)):
    result = services.authenticate_via_firebase(db, body.firebase_token)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticación fallida con Firebase"
        )
    return result
