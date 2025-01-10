from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.sql import func

from ..base import Base


class DialogTable(Base):
    __tablename__ = "dialog_tab"

    id = Column(String(100), primary_key=True)
    user_id = Column(String(100), nullable=False)
    agent_id = Column(String(100), nullable=False)
    sender = Column(Enum("user", "assistant", name="sender_type"), nullable=False)
    content = Column(String(1000), nullable=False)
    type = Column(Enum("message", "command", name="dialog_type"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    platform = Column(Enum("twitter", "telegram_private", "telegram_group", name="platform_type"), nullable=False)
