# Import all the models, so that Base has them before being
# imported by Alembic
from database.base_class import Base  # noqa
from database.models.audit import AuditLog  # noqa
from database.models.user import User, Role, AllowedEmail  # noqa
from database.models.driver import Driver, License, DriverCourse, Fine  # noqa
from database.models.vehicle import Vehicle, VehicleDocument, Maintenance  # noqa
from database.models.inspection import SafeInspection, FirstAidInspection  # noqa
from database.models.cashless import Cashless  # noqa
from database.models.employee import Employee  # noqa





