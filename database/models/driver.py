from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean

from sqlalchemy.orm import relationship
from database.base_class import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    
    # Relationships
    licenses = relationship("License", back_populates="driver")
    courses = relationship("DriverCourse", back_populates="driver")
    fines = relationship("Fine", back_populates="driver")

class License(Base):
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    category = Column(String, nullable=False)
    expiration_date = Column(Date, nullable=False)
    
    driver = relationship("Driver", back_populates="licenses")

class DriverCourse(Base):
    __tablename__ = "driver_courses"
    
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    name = Column(String, nullable=False)
    finish_date = Column(Date, nullable=False)
    
    driver = relationship("Driver", back_populates="courses")

class Fine(Base):
    __tablename__ = "fines"
    
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    amount = Column(Float, nullable=False)
    reason = Column(String, nullable=False)
    is_paid = Column(Boolean, default=False)

    
    driver = relationship("Driver", back_populates="fines")
