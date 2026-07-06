from sqlalchemy.orm import Session
from apps.user.repository import user_repository
from apps.user.schemas import UserCreate

from providers.firebase.auth import firebase_auth
from core.config import settings
from datetime import datetime, timedelta, timezone
from jose import jwt

def authenticate_via_firebase(db: Session, firebase_token: str):
    try:
        # 1. Validar con Firebase
        decoded_token = firebase_auth.verify_id_token(firebase_token)
        uid = decoded_token['uid']
        email = decoded_token.get('email')

        if not email:
            return None

        # 2. Verificar whitelist - solo emails permitidos pueden acceder
        is_allowed = user_repository.is_email_allowed(db, email=email)
        if not is_allowed:
            # Si el usuario ya existe en BD (migración), permitir acceso
            existing_user = user_repository.get_by_email(db, email=email)
            if not existing_user:
                return None

        # 3. Buscar o crear usuario en PostgreSQL
        user = user_repository.get_by_firebase_uid(db, uid=uid)
        if user and not user.is_active:
            return None
        if not user:
            # Buscar por email (usuario pre-creado desde whitelist)
            user = user_repository.get_by_email(db, email=email)
            if user:
                if not user.is_active:
                    return None
                # Vincular firebase_uid al usuario pre-creado
                user.firebase_uid = uid
                user.full_name = decoded_token.get('name', user.full_name)
                user.is_active = True
                db.commit()
                db.refresh(user)
            else:
                user_in = UserCreate(
                    email=email,
                    firebase_uid=uid,
                    full_name=decoded_token.get('name', 'Usuario Nuevo'),
                    is_active=True
                )
                user = user_repository.create(db, obj_in=user_in)
                # Asignar rol 'user' por defecto
                user_repository.assign_role(db, user_id=user.id, role_name="user")

        # 4. Actualizar last_login
        user.last_login = datetime.now(timezone.utc)
        db.commit()

        # 5. Generar JWT Interno
        role_names = [r.name for r in user.roles]
        access_token = create_internal_token({"sub": str(user.id), "uid": uid})

        # Construir respuesta con roles incluidos
        user_data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "firebase_uid": user.firebase_uid,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "roles": role_names,
        }
        return {"access_token": access_token, "token_type": "bearer", "user": user_data}

    except Exception as e:
        return None

def create_internal_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
