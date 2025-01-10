import uuid
from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from teleAgent.daos.twitter_auth.impl import TwitterAuthDAO
from teleAgent.database.base import Base
from teleAgent.database.tables.twitter_auth import TwitterAuth
from teleAgent.models.twitter_auth import TwitterAuthModel


@pytest.fixture
def session_factory():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    return factory


@pytest.fixture
def twitter_auth_dao(session_factory: sessionmaker):
    return TwitterAuthDAO(session_factory)


@pytest.fixture
def test_auth():
    return TwitterAuthModel(
        id="test-auth-1",
        agent_id="test-agent-1",
        access_token="test-access-token",
        refresh_token="test-refresh-token",
        expires_at=datetime.utcnow() + timedelta(hours=1),
    )


def test_create_auth(twitter_auth_dao: TwitterAuthDAO, test_auth: TwitterAuthModel):
    created = twitter_auth_dao.create(test_auth)
    assert created.access_token == test_auth.access_token
    assert created.refresh_token == test_auth.refresh_token
    assert created.agent_id == test_auth.agent_id


def test_get_by_id(twitter_auth_dao: TwitterAuthDAO, test_auth: TwitterAuthModel):
    created = twitter_auth_dao.create(test_auth)
    retrieved = twitter_auth_dao.get_by_id(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.access_token == created.access_token


def test_get_by_id_not_found(twitter_auth_dao: TwitterAuthDAO):
    retrieved = twitter_auth_dao.get_by_id("non-existent")
    assert retrieved is None


@pytest.mark.asyncio
async def test_get_by_agent_id(twitter_auth_dao: TwitterAuthDAO, test_auth: TwitterAuthModel):
    twitter_auth_dao.create(test_auth)
    retrieved = await twitter_auth_dao.get_by_agent_id(test_auth.agent_id)
    assert retrieved is not None
    assert retrieved.agent_id == test_auth.agent_id


def test_update_auth(twitter_auth_dao: TwitterAuthDAO, test_auth: TwitterAuthModel):
    created = twitter_auth_dao.create(test_auth)
    created.access_token = "updated-access-token"
    updated = twitter_auth_dao.update(created)
    assert updated is not None
    assert updated.access_token == "updated-access-token"


@pytest.mark.asyncio
async def test_update_tokens(twitter_auth_dao: TwitterAuthDAO, test_auth: TwitterAuthModel):
    created = twitter_auth_dao.create(test_auth)
    new_expires = datetime.utcnow() + timedelta(hours=2)
    success = await twitter_auth_dao.update_tokens(
        created.id,
        "new-access-token",
        "new-refresh-token",
        new_expires,
    )
    assert success is True
    
    updated = twitter_auth_dao.get_by_id(created.id)
    assert updated is not None
    assert updated.access_token == "new-access-token"
    assert updated.refresh_token == "new-refresh-token"
    assert abs(updated.expires_at - new_expires).total_seconds() < 1


@pytest.mark.asyncio
async def test_list_expiring_soon(twitter_auth_dao: TwitterAuthDAO):
    # Create auth records with different expiry times
    for i in range(3):
        auth = TwitterAuthModel(
            id=f"test-auth-{i}",
            agent_id=f"test-agent-{i}",
            access_token=f"access-token-{i}",
            refresh_token=f"refresh-token-{i}",
            expires_at=datetime.utcnow() + timedelta(hours=i),
        )
        twitter_auth_dao.create(auth)

    expiring = await twitter_auth_dao.list_expiring_soon(within_hours=2)
    assert len(expiring) == 2  # Should return 2 records expiring within 2 hours


@pytest.mark.asyncio
async def test_delete_by_agent_id(twitter_auth_dao: TwitterAuthDAO, test_auth: TwitterAuthModel):
    twitter_auth_dao.create(test_auth)
    success = await twitter_auth_dao.delete_by_agent_id(test_auth.agent_id)
    assert success is True
    
    retrieved = await twitter_auth_dao.get_by_agent_id(test_auth.agent_id)
    assert retrieved is None


def test_delete_auth(twitter_auth_dao: TwitterAuthDAO, test_auth: TwitterAuthModel):
    created = twitter_auth_dao.create(test_auth)
    result = twitter_auth_dao.delete(created.id)
    assert result is True
    
    retrieved = twitter_auth_dao.get_by_id(created.id)
    assert retrieved is None


@pytest.mark.asyncio
async def test_multiple_agents_auth(twitter_auth_dao: TwitterAuthDAO):
    # Create auth records for multiple agents
    auths = []
    for i in range(3):
        auth = TwitterAuthModel(
            id=f"test-auth-{i}",
            agent_id=f"test-agent-{i}",
            access_token=f"access-token-{i}",
            refresh_token=f"refresh-token-{i}",
            expires_at=datetime.utcnow() + timedelta(hours=1),
        )
        auths.append(twitter_auth_dao.create(auth))

    # Verify each agent's auth can be retrieved
    for auth in auths:
        retrieved = await twitter_auth_dao.get_by_agent_id(auth.agent_id)
        assert retrieved is not None
        assert retrieved.agent_id == auth.agent_id


def test_update_nonexistent_auth(twitter_auth_dao: TwitterAuthDAO, test_auth: TwitterAuthModel):
    test_auth.id = "non-existent"
    updated = twitter_auth_dao.update(test_auth)
    assert updated is None