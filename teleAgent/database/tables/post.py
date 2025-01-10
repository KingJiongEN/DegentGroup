from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.sql import func

from ..base import Base


class Post(Base):
    __tablename__ = "post_tab"

    id = Column(String(100), primary_key=True)
    agent_id = Column(String(100), ForeignKey("agent_tab.id"), nullable=False)
    content = Column(String(1000), nullable=False)
    platform = Column(Enum("twitter", "telegram", name="platform_type"), nullable=False)
    external_id = Column(String(100))
    published_at = Column(DateTime(timezone=True), server_default=func.now())
