from abc import abstractmethod
from datetime import datetime
from typing import List, Optional

from teleAgent.daos.base import BaseDAO
from teleAgent.database.tables.twitter_auth import TwitterAuth
from teleAgent.models.twitter_auth import TwitterAuthModel


class ITwitterAuthDAO(BaseDAO[TwitterAuthModel, TwitterAuth]):
    """Twitter Auth DAO interface"""
    
    @abstractmethod
    async def get_by_agent_id(self, agent_id: str) -> Optional[TwitterAuthModel]:
        """Get Twitter auth by agent ID"""
        pass

    @abstractmethod
    async def update_tokens(
        self,
        auth_id: str,
        access_token: str,
        refresh_token: str,
        expires_at: datetime,
    ) -> bool:
        """Update access and refresh tokens"""
        pass

    @abstractmethod
    async def list_expiring_soon(self, within_hours: int = 24) -> List[TwitterAuthModel]:
        """Get auth records that will expire within specified hours"""
        pass

    @abstractmethod
    async def delete_by_agent_id(self, agent_id: str) -> bool:
        """Delete auth record by agent ID"""
        pass