from database.repository.base import BaseRepository
from database.models.cashless import Cashless
from apps.cashless.schemas import CashlessCreate, CashlessUpdate
from sqlalchemy.orm import Session
from typing import Optional

class CashlessRepository(BaseRepository[Cashless, CashlessCreate, CashlessUpdate]):
    def get_by_codigo(self, db: Session, codigo: int) -> Optional[Cashless]:
        return db.query(Cashless).filter(Cashless.codigo == codigo).first()

cashless_repository = CashlessRepository(Cashless)
