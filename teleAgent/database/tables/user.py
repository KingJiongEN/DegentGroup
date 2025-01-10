from sqlalchemy import Column, DateTime, Enum, String
from sqlalchemy.sql import func

from ..base import Base


class User(Base):
    __tablename__ = "user_tab"

    id = Column(String(100), primary_key=True)
    username = Column(String(100), nullable=False)
    platform_id = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True))
    status = Column(
        Enum("active", "inactive", "banned", name="user_status"), default="active"
    )
