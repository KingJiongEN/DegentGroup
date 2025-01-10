from abc import ABC, abstractmethod
from typing import List, Optional

from teleAgent.daos.base import BaseDAO
from teleAgent.database.tables.agent import AgentTable
from teleAgent.models.agent import Agent


class IAgentDAO(BaseDAO[Agent, AgentTable]):
    """Agent DAO 接口"""

    @abstractmethod
    def list_active(self) -> List[Agent]:
        """获取所有活跃的Agent"""
        pass

    @abstractmethod
    def update_balance(self, agent_id: str, new_balance: float) -> bool:
        """更新Agent余额"""
        pass

    @abstractmethod
    def get_by_wallet(self, wallet_address: str) -> Optional[Agent]:
        """根据钱包地址获取Agent"""
        pass
