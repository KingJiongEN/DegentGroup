from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from ..base import Base


class TwitterAuth(Base):
    __tablename__ = "twitter_auth_tab"

    id = Column(String, primary_key=True)
    agent_id = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
