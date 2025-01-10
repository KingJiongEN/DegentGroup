import time
import uuid
from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from teleAgent.daos.dialog.impl import DialogDAO
from teleAgent.database.base import Base
from teleAgent.database.tables.dialog import DialogTable
from teleAgent.models.dialog import Dialog

@pytest.fixture
def session_factory():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    return factory

@pytest.fixture
def dialog_dao(session_factory: sessionmaker):
    return DialogDAO(session_factory)

@pytest.fixture
def test_dialog():
    return Dialog(
        id="test-dialog-1",
        user_id="test-user-1",
        agent_id="test-agent-1",
        content="Test message content",
        type="message",
        platform="telegram",
        created_at=datetime.utcnow(),
    )

def test_create_dialog(dialog_dao: DialogDAO, test_dialog: Dialog):
    created = dialog_dao.create(test_dialog)
    assert created.content == test_dialog.content
    assert created.user_id == test_dialog.user_id
    assert created.agent_id == test_dialog.agent_id
    assert created.type == test_dialog.type
    assert created.platform == test_dialog.platform


def test_get_by_id(dialog_dao: DialogDAO, test_dialog: Dialog):
    created = dialog_dao.create(test_dialog)
    retrieved = dialog_dao.get_by_id(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.content == created.content


def test_get_by_id_not_found(dialog_dao: DialogDAO):
    retrieved = dialog_dao.get_by_id("non-existent")
    assert retrieved is None


def test_update_dialog(dialog_dao: DialogDAO, test_dialog: Dialog):
    created = dialog_dao.create(test_dialog)
    created.content = "Updated content"
    updated = dialog_dao.update(created)
    assert updated is not None
    assert updated.content == "Updated content"


def test_update_nonexistent_dialog(dialog_dao: DialogDAO, test_dialog: Dialog):
    test_dialog.id = "non-existent"
    updated = dialog_dao.update(test_dialog)
    assert updated is None


def test_delete_dialog(dialog_dao: DialogDAO, test_dialog: Dialog):
    created = dialog_dao.create(test_dialog)
    result = dialog_dao.delete(created.id)
    assert result is True
    retrieved = dialog_dao.get_by_id(created.id)
    assert retrieved is None


def test_get_by_session(dialog_dao: DialogDAO, test_dialog: Dialog):
    dialog_dao.create(test_dialog)
    # Create another dialog in the same session
    dialog2 = Dialog(
        id="test-dialog-2",
        user_id=test_dialog.user_id,
        agent_id=test_dialog.agent_id,
        content="Second message",
        type="message",
        platform="telegram",
        created_at=datetime.utcnow(),
    )
    dialog_dao.create(dialog2)

    dialogs = dialog_dao.get_by_session(test_dialog.user_id, test_dialog.agent_id)
    assert len(dialogs) == 2
    assert all(d.user_id == test_dialog.user_id for d in dialogs)
    assert all(d.agent_id == test_dialog.agent_id for d in dialogs)


def test_get_recent(dialog_dao: DialogDAO, test_dialog: Dialog):
    # Create multiple dialogs
    dialog_dao.create(test_dialog)
    for i in range(5):
        dialog = Dialog(
            id=f"test-dialog-{i+2}",
            user_id=f"test-user-{i+2}",
            agent_id=test_dialog.agent_id,
            content=f"Message {i+2}",
            type="message",
            platform="telegram",
            created_at=datetime.utcnow(),
        )
        dialog_dao.create(dialog)

    recent_dialogs = dialog_dao.get_recent(test_dialog.agent_id, limit=3)
    assert len(recent_dialogs) == 3
    assert all(d.agent_id == test_dialog.agent_id for d in recent_dialogs)


def test_get_by_platform(dialog_dao: DialogDAO, test_dialog: Dialog):
    dialog_dao.create(test_dialog)
    # Create dialog for different platform
    twitter_dialog = Dialog(
        id="test-dialog-twitter",
        user_id="test-user-2",
        agent_id="test-agent-2",
        content="Twitter message",
        type="message",
        platform="twitter",
        created_at=datetime.utcnow(),
    )
    dialog_dao.create(twitter_dialog)

    start_time = datetime.utcnow() - timedelta(hours=1)
    end_time = datetime.utcnow() + timedelta(hours=1)

    telegram_dialogs = dialog_dao.get_by_platform("telegram", start_time, end_time)
    assert len(telegram_dialogs) == 1
    assert all(d.platform == "telegram" for d in telegram_dialogs)


def test_get_by_user(dialog_dao: DialogDAO, test_dialog: Dialog):
    dialog_dao.create(test_dialog)
    # Create additional dialogs for same user
    for i in range(3):
        dialog = Dialog(
            id=f"test-dialog-user-{i+2}",
            user_id=test_dialog.user_id,
            agent_id=f"test-agent-{i+2}",
            content=f"User message {i+2}",
            type="message",
            platform="telegram",
            created_at=datetime.utcnow(),
        )
        dialog_dao.create(dialog)

    user_dialogs = dialog_dao.get_by_user(test_dialog.user_id, limit=2)
    assert len(user_dialogs) == 2
    assert all(d.user_id == test_dialog.user_id for d in user_dialogs)


def test_delete_expired(dialog_dao: DialogDAO):
    """Test deleting expired dialog records"""
    # Create an old dialog record
    old_time = datetime.utcnow() - timedelta(days=2)
    old_dialog = Dialog(
        id=str(uuid.uuid4()),
        user_id="test_user_1",
        agent_id="test_agent_1",
        content="Old message",
        type="message",
        platform="telegram",
        created_at=old_time,
    )
    dialog_dao.create(old_dialog)

    # Add delay to ensure timestamp difference
    time.sleep(0.1)  # 100ms delay

    # Create a new dialog record
    recent_dialog = Dialog(
        id=str(uuid.uuid4()),
        user_id="test_user_1",
        agent_id="test_agent_1",
        content="Recent message",
        type="message",
        platform="telegram",
        created_at=datetime.utcnow(),
    )
    dialog_dao.create(recent_dialog)

    # Add another delay
    time.sleep(0.1)  # 100ms delay

    # Delete records older than 1 day
    expire_time = datetime.utcnow() - timedelta(days=1)
    deleted_count = dialog_dao.delete_expired(expire_time)

    # Verify delete count
    assert deleted_count == 1

    # Verify only recent record remains
    remaining_dialogs = dialog_dao.get_by_platform(
        "telegram", datetime.utcnow() - timedelta(days=7), datetime.utcnow()
    )
    assert len(remaining_dialogs) == 1
    assert remaining_dialogs[0].id == recent_dialog.id