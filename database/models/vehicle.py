from sqlalchemy import Column, Integer, String, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database.base_class import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String, unique=True, index=True, nullable=False)
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    
    # Relationships
    documents = relationship("VehicleDocument", back_populates="vehicle")
    maintenances = relationship("Maintenance", back_populates="vehicle")

class VehicleDocument(Base):
    __tablename__ = "vehicle_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    document_type = Column(String, nullable=False) # SOAT, RTM, etc.
    expiration_date = Column(Date, nullable=False)
    file_url = Column(String, nullable=True) # Link to Firebase Storage
    
    vehicle = relationship("Vehicle", back_populates="documents")

class Maintenance(Base):
    __tablename__ = "maintenance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    details = Column(JSON, nullable=True)
    
    vehicle = relationship("Vehicle", back_populates="maintenances")
