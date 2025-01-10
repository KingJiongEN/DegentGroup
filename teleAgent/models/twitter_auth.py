from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TwitterAuthModel(BaseModel):
    """Twitter Auth Model"""
    id: str
    agent_id: str
    access_token: str
    refresh_token: str
    expires_at: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True