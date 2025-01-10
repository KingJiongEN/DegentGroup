from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from ..base import Base


class Memory(Base):
    __tablename__ = "memorie_tab"

    id = Column(String(100), primary_key=True)
    agent_id = Column(String(100), ForeignKey("agent_tab.id"), nullable=False)
    context = Column(String(2000), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expire_at = Column(DateTime(timezone=True), nullable=False)
    priority = Column(Integer, default=0)
