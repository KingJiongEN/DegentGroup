from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from teleAgent.daos.base import BaseDAO
from teleAgent.database.tables.dialog import DialogTable
from teleAgent.models.dialog import Dialog


class IDialogDAO(BaseDAO[Dialog, DialogTable]):
    """Dialog DAO Interface"""

    @abstractmethod
    def get_by_session(self, user_id: str, agent_id: str) -> List[Dialog]:
        """获取指定用户和Agent之间的对话记录"""
        pass

    @abstractmethod
    def get_recent(self, agent_id: str, limit: int = 10) -> List[Dialog]:
        """获取Agent最近的对话记录"""
        pass

    @abstractmethod
    def get_by_platform(
        self, platform: str, start_time: datetime, end_time: datetime
    ) -> List[Dialog]:
        """获取指定平台在时间范围内的对话记录"""
        pass

    @abstractmethod
    def get_by_user(self, user_id: str, limit: int = 20) -> List[Dialog]:
        """获取用户的最近对话记录"""
        pass

    @abstractmethod
    def delete_expired(self, before_time: datetime) -> int:
        """删除指定时间之前的对话记录"""
        pass
