from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from database.base_class import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # Firebase UID or local ID
    action = Column(String, nullable=False)  # CREATE, UPDATE, DELETE
    table_affected = Column(String, nullable=False)
    data_old = Column(JSON, nullable=True)
    data_new = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
