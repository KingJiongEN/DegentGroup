import uuid
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from teleAgent.daos.nft.impl import NFTDAO
from teleAgent.database.base import Base
from teleAgent.models.nft import NFT, NFTMetadata, NFTStatus
from teleAgent.database.tables.agent import AgentTable

@pytest.fixture
def session_factory():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    # Create a test agent
    Session = sessionmaker(bind=engine)
    with Session() as session:
        test_agent = AgentTable(
            id="test-agent-1",
            name="Test Agent",
            personality="Test Personality",
            configs={},
            stats={},
            is_active=True
        )
        session.add(test_agent)
        session.commit()
    
    return sessionmaker(bind=engine)

@pytest.fixture
def nft_dao(session_factory):
    return NFTDAO(session_factory)

@pytest.fixture
def test_nft():
    metadata = NFTMetadata(
        name="Test NFT",
        description="A test NFT artwork",
        image_url="/path/to/image.png",
        art_style="pop_art",
        attributes={"trait": "value"},
        background_story="Test poem",
        creation_context="Test analysis"
    )
    
    return NFT(
        id=str(uuid.uuid4()),
        token_id="token-1",
        contract_address="0x123...",
        metadata=metadata,
        creator_id="test-agent-1",
        owner_id="test-agent-1",
        status=NFTStatus.DRAFT,
        created_at=datetime.utcnow()
    )

def test_create_nft(nft_dao, test_nft):
    created = nft_dao.create(test_nft)
    assert created.metadata.name == test_nft.metadata.name
    assert created.creator_id == test_nft.creator_id
    assert created.owner_id == test_nft.creator_id

def test_get_by_id(nft_dao, test_nft):
    created = nft_dao.create(test_nft)
    retrieved = nft_dao.get_by_id(created.id)
    assert retrieved is not None
    assert retrieved.metadata.name == created.metadata.name

def test_get_by_creator(nft_dao, test_nft):
    nft_dao.create(test_nft)
    nfts = nft_dao.get_by_creator(test_nft.creator_id)
    assert len(nfts) == 1
    assert nfts[0].creator_id == test_nft.creator_id

def test_get_by_owner(nft_dao, test_nft):
    created = nft_dao.create(test_nft)
    nfts = nft_dao.get_by_owner(created.owner_id)
    assert len(nfts) == 1
    assert nfts[0].owner_id == created.owner_id 

def test_update_nft(nft_dao, test_nft):
    # First create an NFT
    created = nft_dao.create(test_nft)
    
    # Modify some fields
    created.metadata.name = "Updated NFT Name"
    created.metadata.description = "Updated description"
    created.status = NFTStatus.MINTED
    
    # Update in database
    updated = nft_dao.update(created)
    
    # Verify updates
    assert updated is not None
    assert updated.metadata.name == "Updated NFT Name"
    assert updated.metadata.description == "Updated description"
    assert updated.status == NFTStatus.MINTED

def test_update_nonexistent_nft(nft_dao, test_nft):
    # Try to update NFT that doesn't exist
    test_nft.id = "nonexistent-id"
    updated = nft_dao.update(test_nft)
    assert updated is None

def test_delete_nft(nft_dao, test_nft):
    # First create an NFT
    created = nft_dao.create(test_nft)
    
    # Delete it
    result = nft_dao.delete(created.id)
    assert result is True
    
    # Verify it's gone
    retrieved = nft_dao.get_by_id(created.id)
    assert retrieved is None

def test_delete_nonexistent_nft(nft_dao):
    # Try to delete NFT that doesn't exist
    result = nft_dao.delete("nonexistent-id")
    assert result is False