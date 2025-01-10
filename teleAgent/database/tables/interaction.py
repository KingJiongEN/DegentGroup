from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.sql import func

from ..base import Base


class Interaction(Base):
    __tablename__ = "interaction_tab"

    id = Column(String(100), primary_key=True)
    post_id = Column(String(100), ForeignKey("post_tab.id"), nullable=False)
    user_id = Column(String(100), ForeignKey("user_tab.id"), nullable=False)
    type = Column(
        Enum("like", "retweet", "reply", name="interaction_type"), nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
