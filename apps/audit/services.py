from sqlalchemy.orm import Session
from database.models.audit import AuditLog
from sqlalchemy import desc

def get_all_audit_logs_service(db: Session, limit: int = 100):
    return db.query(AuditLog).order_by(desc(AuditLog.timestamp)).limit(limit).all()
