from typing import List, Optional

from sqlalchemy.orm import Session, sessionmaker

from teleAgent.database.tables.agent import AgentTable
from teleAgent.models.agent import Agent
from teleAgent.daos.base import BaseDAO
from .interface import IAgentDAO

class AgentDAO(IAgentDAO):
    def __init__(self, session_factory: sessionmaker):
        super().__init__(session_factory)

    def _to_model(self, table: AgentTable) -> Agent:
        return Agent(
            id=table.id,
            name_str=table.name,
            personality=table.personality,
            art_style=table.art_style,
            profile=table.profile,
            avatar=table.avatar,
            configs=table.configs or {},
            stats=table.stats or {},
            wallet_address=table.wallet_address,
            is_active=table.is_active,
        )

    def get_by_id(self, agent_id: str) -> Optional[Agent]:
        with self._get_session() as session:
            table = session.query(AgentTable).get(agent_id)
            return self._to_model(table) if table else None

    def list_active(self) -> List[Agent]:
        with self._get_session() as session:
            tables = session.query(AgentTable).filter(AgentTable.is_active == True).all()
            return [self._to_model(t) for t in tables]

    def create(self, agent: Agent) -> Agent:
        with self._get_session() as session:
            table = AgentTable(
                id=agent.id,
                name=agent.name_str,
                personality=agent.personality,
                profile=agent.profile,
                avatar=agent.avatar,
                configs=agent.configs,
                stats=agent.stats,
                wallet_address=agent.wallet_address,
                is_active=agent.is_active,
            )
            session.add(table)
            session.flush()
            return self._to_model(table)

    def update(self, agent: Agent) -> Optional[Agent]:
        with self._get_session() as session:
            table = session.query(AgentTable).get(agent.id)
            if not table:
                return None
            self._update_table(table, agent)
            return self._to_model(table)

    def _update_table(self, table: AgentTable, agent: Agent) -> None:
        """Update table instance with agent model data"""
        table.name = agent.name_str
        table.personality = agent.personality
        table.profile = agent.profile
        table.avatar = agent.avatar
        table.configs = agent.configs
        table.stats = agent.stats
        table.wallet_address = agent.wallet_address
        table.is_active = agent.is_active

    def delete(self, agent_id: str) -> bool:
        with self._get_session() as session:
            rows = session.query(AgentTable).filter(AgentTable.id == agent_id).delete()
            return rows > 0

    def update_balance(self, agent_id: str, new_balance: float) -> bool:
        raise NotImplementedError("update_balance is not implemented")
        with self._get_session() as session:
            rows = (
                session.query(AgentTable)
                .filter(AgentTable.id == agent_id)
                .update({AgentTable.balance: new_balance})
            )
            return rows > 0

    def get_by_wallet(self, wallet_address: str) -> Optional[Agent]:
        with self._get_session() as session:
            table = (
                session.query(AgentTable)
                .filter(AgentTable.wallet_address == wallet_address)
                .first()
            )
            return self._to_model(table) if table else None