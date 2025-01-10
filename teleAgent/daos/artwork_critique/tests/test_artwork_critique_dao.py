import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from teleAgent.database.base import Base
from teleAgent.database.tables.nft import NFTTable
from teleAgent.database.tables.agent import AgentTable
from teleAgent.database.tables.artwork_critique import ArtworkCritiqueTable
from teleAgent.daos.artwork_critique.impl import ArtworkCritiqueDAO
from teleAgent.models.artwork_critique import ArtworkCritique

@pytest.fixture
def session_factory():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create test agent
    test_agent = AgentTable(
        id="test-agent-1",
        name="Test Agent",
        personality="Test Personality",
        configs={},
        stats={}
    )
    session.add(test_agent)
    
    # Create test NFT
    test_nft = NFTTable(
        id="test-nft-1",
        name="Test NFT",
        image_path="/path/to/image.jpg",
        art_style="impressionist",
        creator_id="test-agent-1",
        current_owner_id="test-agent-1",
        attributes={},
        status="draft"
    )
    session.add(test_nft)
    session.commit()
    session.close()
    
    return sessionmaker(bind=engine)

@pytest.fixture
def artwork_critique_dao(session_factory):
    return ArtworkCritiqueDAO(session_factory)

@pytest.fixture
def test_critique():
    return ArtworkCritique(
        id="test-critique-1",
        nft_id="test-nft-1",
        critic_agent_id="test-agent-1",
        critic_agent_name="Test Critic",
        critique_details={
            "style_match": "Good match with post-impressionist style",
            "style_match_score": 8,
            "emotional_impact": "Strong emotional resonance",
            "emotional_impact_score": 9,
            "harmony": "Well balanced composition",
            "harmony_score": 7,
            "areas_for_improvement": "Could improve color contrast"
        },
        overall_score=8.0,
        created_at=datetime.utcnow()
    )

def test_create_critique(artwork_critique_dao, test_critique):
    created = artwork_critique_dao.create(test_critique)
    assert created.id == test_critique.id
    assert created.critic_agent_name == test_critique.critic_agent_name
    assert created.overall_score == test_critique.overall_score

def test_get_by_nft_id(artwork_critique_dao, test_critique):
    created = artwork_critique_dao.create(test_critique)
    critiques = artwork_critique_dao.get_by_nft_id(created.nft_id)
    assert len(critiques) == 1
    assert critiques[0].id == created.id

def test_get_by_critic_id(artwork_critique_dao, test_critique):
    created = artwork_critique_dao.create(test_critique)
    critiques = artwork_critique_dao.get_by_critic_id(created.critic_agent_id)
    assert len(critiques) == 1
    assert critiques[0].id == created.id 

def test_get_by_critic_nft_id(artwork_critique_dao, test_critique):
    # Create the test critique
    created = artwork_critique_dao.create(test_critique)
    
    # Test getting by both critic ID and NFT ID
    retrieved = artwork_critique_dao.get_by_critic_nft_id(
        created.critic_agent_id,
        created.nft_id
    )
    
    assert retrieved.id == created.id
    assert retrieved.critic_agent_id == created.critic_agent_id
    assert retrieved.nft_id == created.nft_id
    
    # Test with non-existent IDs
    not_found = artwork_critique_dao.get_by_critic_nft_id(
        "non-existent-critic",
        "non-existent-nft"
    )
    assert not_found is None

def test_get_by_id_not_found(artwork_critique_dao):
    """Test getting a non-existent critique by ID"""
    result = artwork_critique_dao.get_by_id("non-existent-id")
    assert result is None

def test_update_critique(artwork_critique_dao, test_critique):
    """Test updating an existing critique"""
    # First create the critique
    created = artwork_critique_dao.create(test_critique)
    
    # Modify some fields
    created.critique_details["new_field"] = "new value"
    created.overall_score = 9.0
    
    # Update
    updated = artwork_critique_dao.update(created)
    assert updated is not None
    assert updated.overall_score == 9.0
    assert updated.critique_details["new_field"] == "new value"

def test_update_nonexistent_critique(artwork_critique_dao, test_critique):
    """Test updating a non-existent critique"""
    test_critique.id = "non-existent-id"
    result = artwork_critique_dao.update(test_critique)
    assert result is None

def test_delete_critique(artwork_critique_dao, test_critique):
    """Test deleting an existing critique"""
    # First create the critique
    created = artwork_critique_dao.create(test_critique)
    
    # Delete it
    result = artwork_critique_dao.delete(created.id)
    assert result is True
    
    # Verify it's gone
    retrieved = artwork_critique_dao.get_by_id(created.id)
    assert retrieved is None

def test_delete_nonexistent_critique(artwork_critique_dao):
    """Test deleting a non-existent critique"""
    result = artwork_critique_dao.delete("non-existent-id")
    assert result is False

def test_get_by_nft_id_not_found(artwork_critique_dao):
    """Test getting critiques for a non-existent NFT"""
    critiques = artwork_critique_dao.get_by_nft_id("non-existent-nft")
    assert len(critiques) == 0

def test_get_by_critic_id_not_found(artwork_critique_dao):
    """Test getting critiques by a non-existent critic"""
    critiques = artwork_critique_dao.get_by_critic_id("non-existent-critic")
    assert len(critiques) == 0

def test_get_by_critic_nft_id_not_found(artwork_critique_dao):
    """Test getting a non-existent critique by critic and NFT IDs"""
    result = artwork_critique_dao.get_by_critic_nft_id("non-existent-critic", "non-existent-nft")
    assert result is None