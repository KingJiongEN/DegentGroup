import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from teleAgent.daos.agent.impl import AgentDAO
from teleAgent.database.base import Base
from teleAgent.database.tables.agent import AgentTable
from teleAgent.models.agent import Agent


@pytest.fixture
def session_factory():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    return factory


@pytest.fixture
def agent_dao(session_factory: sessionmaker):
    return AgentDAO(session_factory)


@pytest.fixture
def test_agent():
    return Agent(
        id="test-id-1",
        name="TestAgent",
        personality="Test Personality",
        art_style="test_art_style",
        profile="Test Profile",
        avatar="test.jpg",
        configs={},
        stats={},
        wallet_address="test-wallet-1",
        balance=100.0,
        is_active=True,
    )


def test_create_agent(agent_dao: AgentDAO, test_agent: Agent):
    created = agent_dao.create(test_agent)
    assert created.name == test_agent.name
    assert created.wallet_address == test_agent.wallet_address


def test_get_by_id(agent_dao: AgentDAO, test_agent: Agent):
    created = agent_dao.create(test_agent)
    retrieved = agent_dao.get_by_id(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.name == created.name


def test_get_by_id_not_found(agent_dao: AgentDAO):
    retrieved = agent_dao.get_by_id("non-existent")
    assert retrieved is None


def test_list_active(agent_dao: AgentDAO, test_agent: Agent):
    agent_dao.create(test_agent)
    inactive_agent = Agent(
        id="test-id-2",
        name="Inactive",
        personality="Test",
        art_style="test art style",
        is_active=False,
        wallet_address="test-wallet-2",
        balance=0.0,
        configs={},
        stats={},
    )
    agent_dao.create(inactive_agent)

    active_agents = agent_dao.list_active()
    assert len(active_agents) == 1
    assert active_agents[0].name == test_agent.name


def test_update_agent(agent_dao: AgentDAO, test_agent: Agent):
    created = agent_dao.create(test_agent)
    created.name = "Updated Name"
    updated = agent_dao.update(created)
    assert updated is not None
    assert updated.name == "Updated Name"


def test_delete_agent(agent_dao: AgentDAO, test_agent: Agent):
    created = agent_dao.create(test_agent)
    result = agent_dao.delete(created.id)
    assert result is True
    retrieved = agent_dao.get_by_id(created.id)
    assert retrieved is None


def test_update_balance(agent_dao: AgentDAO, test_agent: Agent):
    created = agent_dao.create(test_agent)
    result = agent_dao.update_balance(created.id, 200.0)
    assert result is True
    updated = agent_dao.get_by_id(created.id)
    assert updated is not None
    assert updated.balance == 200.0


def test_get_by_wallet(agent_dao: AgentDAO, test_agent: Agent):
    agent_dao.create(test_agent)
    retrieved = agent_dao.get_by_wallet(test_agent.wallet_address)
    assert retrieved is not None
    assert retrieved.wallet_address == test_agent.wallet_address