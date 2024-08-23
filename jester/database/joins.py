from sqlalchemy import Column, DateTime, ForeignKey
from jester.database.tables import Base

class AdminActivity(Base):

    admin_id = Column(ForeignKey("admin.id"), primary_key=True)
    """The organization"""

    activity = Column(ForeignKey("activity_type.uuid"), primary_key=True)

    timestamp = Column(DateTime)
