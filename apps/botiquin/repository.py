from database.repository.base import BaseRepository
from database.models.inspection import FirstAidInspection
from apps.botiquin.schemas import FirstAidInspectionCreate, FirstAidInspectionUpdate

class FirstAidInspectionRepository(BaseRepository[FirstAidInspection, FirstAidInspectionCreate, FirstAidInspectionUpdate]):
    pass

first_aid_repository = FirstAidInspectionRepository(FirstAidInspection)
