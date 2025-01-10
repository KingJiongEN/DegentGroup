from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import sessionmaker

from teleAgent.database.tables.dialog import DialogTable
from teleAgent.models.dialog import Dialog
from teleAgent.daos.base import BaseDAO
from .interface import IDialogDAO

class DialogDAO(IDialogDAO):
    def __init__(self, session_factory: sessionmaker):
        super().__init__(session_factory)

    def _to_model(self, table: DialogTable) -> Dialog:
        return Dialog(
            id=table.id,
            user_id=table.user_id,
            agent_id=table.agent_id,
            sender=table.sender,
            content=table.content,
            type=table.type,
            created_at=table.created_at,
            platform=table.platform,
        )

    def get_by_id(self, dialog_id: str) -> Optional[Dialog]:
        with self._get_session() as session:
            table = session.query(DialogTable).filter(DialogTable.id == dialog_id).first()
            return self._to_model(table) if table else None

    def create(self, dialog: Dialog) -> Dialog:
        with self._get_session() as session:
            table = DialogTable(
                id=dialog.id,
                user_id=dialog.user_id,
                agent_id=dialog.agent_id,
                sender=dialog.sender,
                content=dialog.content,
                type=dialog.type,
                platform=dialog.platform,
                created_at=dialog.created_at,
            )
            session.add(table)
            session.flush()
            return self._to_model(table)

    def update(self, dialog: Dialog) -> Optional[Dialog]:
        with self._get_session() as session:
            table = session.query(DialogTable).filter(DialogTable.id == dialog.id).first()
            if not table:
                return None

            table.content = dialog.content
            table.type = dialog.type
            table.platform = dialog.platform
            
            return self._to_model(table)

    def delete(self, dialog_id: str) -> bool:
        with self._get_session() as session:
            rows = session.query(DialogTable).filter(DialogTable.id == dialog_id).delete()
            return rows > 0

    def get_by_session(self, user_id: str, agent_id: str) -> List[Dialog]:
        with self._get_session() as session:
            tables = (
                session.query(DialogTable)
                .filter(DialogTable.user_id == user_id, DialogTable.agent_id == agent_id)
                .order_by(DialogTable.created_at.desc())
                .all()
            )
            return [self._to_model(t) for t in tables]

    def get_recent(self, agent_id: str, limit: int = 10) -> List[Dialog]:
        with self._get_session() as session:
            tables = (
                session.query(DialogTable)
                .filter(DialogTable.agent_id == agent_id)
                .order_by(DialogTable.created_at.desc())
                .limit(limit)
                .all()
            )
            return [self._to_model(t) for t in tables]

    def get_by_platform(
        self, platform: str, start_time: datetime, end_time: datetime
    ) -> List[Dialog]:
        with self._get_session() as session:
            tables = (
                session.query(DialogTable)
                .filter(
                    DialogTable.platform == platform,
                    DialogTable.created_at >= start_time,
                    DialogTable.created_at <= end_time,
                )
                .order_by(DialogTable.created_at.desc())
                .all()
            )
            return [self._to_model(t) for t in tables]

    def get_by_user(self, user_id: str, limit: int = 20) -> List[Dialog]:
        with self._get_session() as session:
            tables = (
                session.query(DialogTable)
                .filter(DialogTable.user_id == user_id)
                .order_by(DialogTable.created_at.desc())
                .limit(limit)
                .all()
            )
            return [self._to_model(t) for t in tables]

    def get_by_user_and_agent(self, user_id: str, agent_id: str) -> List[Dialog]:
        with self._get_session() as session:
            tables = (
                session.query(DialogTable)
                .filter(DialogTable.user_id == user_id, DialogTable.agent_id == agent_id)
                .order_by(DialogTable.created_at.desc())
                .all()
            )
            return [self._to_model(t) for t in tables]

    def delete_expired(self, before_time: datetime) -> int:
        with self._get_session() as session:
            deleted_count = (
                session.query(DialogTable)
                .filter(DialogTable.created_at < before_time)
                .delete(synchronize_session=False)
            )
            return deleted_count

    def delete_by_user_and_agent(self, user_id: str, agent_id: str) -> int:
        dialogs = self.get_by_user_and_agent(user_id, agent_id)
        for dialog in dialogs:
            self.delete(dialog.id)
        return len(dialogs)
