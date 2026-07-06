from database.repository.base import BaseRepository
from database.models.user import User, Role, AllowedEmail
from apps.user.schemas import UserCreate, UserUpdate

from sqlalchemy.orm import Session
from typing import Optional, List

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_firebase_uid(self, db: Session, *, uid: str) -> Optional[User]:
        return db.query(User).filter(User.firebase_uid == uid).first()

    def get_roles(self, db: Session, *, user_id: int) -> List[Role]:
        user = self.get(db, id=user_id)
        if user:
            return user.roles
        return []

    def assign_role(self, db: Session, *, user_id: int, role_name: str) -> Optional[User]:
        user = self.get(db, id=user_id)
        if not user:
            return None
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            return None
        if role not in user.roles:
            user.roles.append(role)
            db.commit()
            db.refresh(user)
        return user

    def remove_role(self, db: Session, *, user_id: int, role_name: str) -> Optional[User]:
        user = self.get(db, id=user_id)
        if not user:
            return None
        role = db.query(Role).filter(Role.name == role_name).first()
        if role and role in user.roles:
            user.roles.remove(role)
            db.commit()
            db.refresh(user)
        return user

    def is_email_allowed(self, db: Session, *, email: str) -> bool:
        return db.query(AllowedEmail).filter(AllowedEmail.email == email).first() is not None

    def add_allowed_email(self, db: Session, *, email: str, created_by: int) -> AllowedEmail:
        entry = AllowedEmail(email=email, created_by=created_by)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    def remove_allowed_email(self, db: Session, *, entry_id: int) -> Optional[AllowedEmail]:
        entry = db.query(AllowedEmail).filter(AllowedEmail.id == entry_id).first()
        if entry:
            db.delete(entry)
            db.commit()
        return entry

    def get_allowed_emails(self, db: Session) -> List[AllowedEmail]:
        return db.query(AllowedEmail).all()

    def get_role_by_name(self, db: Session, *, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()

    def get_all_roles(self, db: Session) -> List[Role]:
        return db.query(Role).all()

user_repository = UserRepository(User)
