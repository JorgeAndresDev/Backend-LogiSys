from database.repository.base import BaseRepository
from database.models.inspection import SafeInspection
from apps.safe.schemas import SafeInspectionCreate, SafeInspectionUpdate

class SafeInspectionRepository(BaseRepository[SafeInspection, SafeInspectionCreate, SafeInspectionUpdate]):
    pass

safe_inspection_repository = SafeInspectionRepository(SafeInspection)
