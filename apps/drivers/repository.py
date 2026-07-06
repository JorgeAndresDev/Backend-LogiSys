from database.repository.base import BaseRepository
from database.models.driver import Driver
from apps.drivers.schemas import DriverCreate, DriverUpdate
from sqlalchemy.orm import Session
from typing import Optional

class DriverRepository(BaseRepository[Driver, DriverCreate, DriverUpdate]):
    def get_by_cedula(self, db: Session, *, cedula: str) -> Optional[Driver]:
        return db.query(Driver).filter(Driver.cedula == cedula).first()

driver_repository = DriverRepository(Driver)
