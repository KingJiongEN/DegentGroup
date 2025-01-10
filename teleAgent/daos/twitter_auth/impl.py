from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from teleAgent.database.tables.twitter_auth import TwitterAuth
from teleAgent.models.twitter_auth import TwitterAuthModel
from teleAgent.daos.base import BaseDAO
from .interface import ITwitterAuthDAO


class TwitterAuthDAO(ITwitterAuthDAO):
    def __init__(self, session_factory: sessionmaker):
        super().__init__(session_factory)

    def _to_model(self, table: TwitterAuth) -> TwitterAuthModel:
        return TwitterAuthModel(
            id=table.id,
            agent_id=table.agent_id,
            access_token=table.access_token,
            refresh_token=table.refresh_token,
            expires_at=table.expires_at,
            created_at=table.created_at,
            updated_at=table.updated_at,
        )

    def get_by_id(self, auth_id: str) -> Optional[TwitterAuthModel]:
        with self._get_session() as session:
            table = session.query(TwitterAuth).filter(TwitterAuth.id == auth_id).first()
            return self._to_model(table) if table else None

    async def get_by_agent_id(self, agent_id: str) -> Optional[TwitterAuthModel]:
        with self._get_session() as session:
            table = (
                session.query(TwitterAuth)
                .filter(TwitterAuth.agent_id == agent_id)
                .first()
            )
            return self._to_model(table) if table else None

    def create(self, auth: TwitterAuthModel) -> TwitterAuthModel:
        with self._get_session() as session:
            table = TwitterAuth(
                id=auth.id,
                agent_id=auth.agent_id,
                access_token=auth.access_token,
                refresh_token=auth.refresh_token,
                expires_at=auth.expires_at,
            )
            session.add(table)
            session.flush()
            return self._to_model(table)

    def update(self, auth: TwitterAuthModel) -> Optional[TwitterAuthModel]:
        with self._get_session() as session:
            table = session.query(TwitterAuth).filter(TwitterAuth.id == auth.id).first()
            if not table:
                return None

            self._update_table(table, auth)
            return self._to_model(table)

    def _update_table(self, table: TwitterAuth, auth: TwitterAuthModel) -> None:
        table.access_token = auth.access_token
        table.refresh_token = auth.refresh_token
        table.expires_at = auth.expires_at

    def delete(self, auth_id: str) -> bool:
        with self._get_session() as session:
            rows = session.query(TwitterAuth).filter(TwitterAuth.id == auth_id).delete()
            return rows > 0

    async def update_tokens(
        self,
        auth_id: str,
        access_token: str,
        refresh_token: str,
        expires_at: datetime,
    ) -> bool:
        with self._get_session() as session:
            rows = (
                session.query(TwitterAuth)
                .filter(TwitterAuth.id == auth_id)
                .update(
                    {
                        TwitterAuth.access_token: access_token,
                        TwitterAuth.refresh_token: refresh_token,
                        TwitterAuth.expires_at: expires_at,
                    }
                )
            )
            return rows > 0

    async def list_expiring_soon(self, within_hours: int = 24) -> List[TwitterAuthModel]:
        with self._get_session() as session:
            expiry_threshold = datetime.utcnow() + timedelta(hours=within_hours)
            tables = (
                session.query(TwitterAuth)
                .filter(
                    and_(
                        TwitterAuth.expires_at <= expiry_threshold,
                        TwitterAuth.expires_at > datetime.utcnow(),
                    )
                )
                .all()
            )
            return [self._to_model(t) for t in tables]

    async def delete_by_agent_id(self, agent_id: str) -> bool:
        with self._get_session() as session:
            rows = (
                session.query(TwitterAuth)
                .filter(TwitterAuth.agent_id == agent_id)
                .delete()
            )
            return rows > 0