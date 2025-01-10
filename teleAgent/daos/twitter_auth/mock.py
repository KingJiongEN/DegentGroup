from datetime import datetime, timedelta
from typing import List, Optional
from unittest.mock import AsyncMock

from teleAgent.daos.twitter_auth.interface import ITwitterAuthDAO
from teleAgent.database.tables.twitter_auth import TwitterAuth
from teleAgent.models.twitter_auth import TwitterAuthModel


class TwitterAuthDAOMock(ITwitterAuthDAO):
    def __init__(self):
        self.storage: dict[str, TwitterAuthModel] = {}
        self.agent_index: dict[str, str] = {}  # agent_id -> auth_id mapping

    async def create(self, model: TwitterAuthModel) -> TwitterAuthModel:
        self.storage[model.id] = model
        self.agent_index[model.agent_id] = model.id
        return model

    async def get_by_id(self, id: str) -> Optional[TwitterAuthModel]:
        return self.storage.get(id)

    async def get_by_agent_id(self, agent_id: str) -> Optional[TwitterAuthModel]:
        auth_id = self.agent_index.get(agent_id)
        if auth_id:
            return self.storage.get(auth_id)
        return None

    async def update(self, id: str, model: TwitterAuthModel) -> bool:
        if id not in self.storage:
            return False
        self.storage[id] = model
        self.agent_index[model.agent_id] = id
        return True

    async def delete(self, id: str) -> bool:
        if id not in self.storage:
            return False
        model = self.storage[id]
        del self.storage[id]
        del self.agent_index[model.agent_id]
        return True

    async def list_all(self) -> List[TwitterAuthModel]:
        return list(self.storage.values())

    async def update_tokens(
        self,
        auth_id: str,
        access_token: str,
        refresh_token: str,
        expires_at: datetime,
    ) -> bool:
        if auth_id not in self.storage:
            return False
            
        model = self.storage[auth_id]
        model.access_token = access_token
        model.refresh_token = refresh_token
        model.expires_at = expires_at
        return True

    async def list_expiring_soon(self, within_hours: int = 24) -> List[TwitterAuthModel]:
        expiry_threshold = datetime.utcnow() + timedelta(hours=within_hours)
        return [
            model for model in self.storage.values() 
            if model.expires_at <= expiry_threshold
        ]

    async def delete_by_agent_id(self, agent_id: str) -> bool:
        auth_id = self.agent_index.get(agent_id)
        if not auth_id:
            return False
        return await self.delete(auth_id)

    def to_model(self, entity: TwitterAuth) -> TwitterAuthModel:
        # Mock implementation - not needed for testing
        pass

    def to_entity(self, model: TwitterAuthModel) -> TwitterAuth:
        # Mock implementation - not needed for testing
        pass