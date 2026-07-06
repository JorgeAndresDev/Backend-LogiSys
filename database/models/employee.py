from sqlalchemy import Column, Integer, String
from database.base_class import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    cc = Column(String(20), unique=True, index=True, nullable=False) # Cedula
    name = Column(String(255), nullable=False)
    cargo = Column(String(100))
    area = Column(String(100))
    phone = Column(String(20))
