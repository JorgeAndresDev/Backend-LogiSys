from database.repository.base import BaseRepository
from database.models.vehicle import Vehicle
from apps.vehicles.schemas import VehicleCreate, VehicleUpdate
from sqlalchemy.orm import Session
from typing import Optional

class VehicleRepository(BaseRepository[Vehicle, VehicleCreate, VehicleUpdate]):
    def get_by_plate(self, db: Session, *, plate: str) -> Optional[Vehicle]:
        return db.query(Vehicle).filter(Vehicle.plate == plate).first()

vehicle_repository = VehicleRepository(Vehicle)
