from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from teleAgent.core.config import settings
from teleAgent.daos.nft.impl import NFTDAO
from teleAgent.daos.agent.impl import AgentDAO
from teleAgent.daos.artwork_critique.impl import ArtworkCritiqueDAO
from teleAgent.models.nft import NFT, NFTMetadata, NFTStatus
from teleAgent.models.agent import Agent
from teleAgent.models.artwork_critique import ArtworkCritique
from teleAgent.database.base import Base
from datetime import datetime
import uuid

def init_db():
    """Initialize database and create all tables"""
    engine = create_engine(settings.DATABASE_URL)
    try:
        Base.metadata.create_all(engine)
        print("✅ Database tables created successfully")
        return engine
    except Exception as e:
        print(f"❌ Error creating database tables: {str(e)}")
        return None

def clean_test_data():
    """Clean up any existing test data"""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # Delete test data in correct order (due to foreign keys)
            conn.execute(text("DELETE FROM artwork_critique_tab WHERE critic_agent_id LIKE 'test-%'"))
            conn.execute(text("DELETE FROM nft_tab WHERE creator_id LIKE 'test-%'"))
            conn.execute(text("DELETE FROM agent_tab WHERE id LIKE 'test-%'"))
            conn.commit()
            print("✅ Cleaned up existing test data")
        except Exception as e:
            print(f"❌ Error cleaning test data: {str(e)}")
            conn.rollback()

def setup_test_data():
    engine = init_db()
    if not engine:
        return None, None, None
        
    SessionLocal = sessionmaker(bind=engine)
    
    # Clean existing test data first
    clean_test_data()
    
    # Initialize DAOs
    agent_dao = AgentDAO(SessionLocal)
    nft_dao = NFTDAO(SessionLocal)
    critique_dao = ArtworkCritiqueDAO(SessionLocal)
    
    try:
        # 1. Create test agent with unique IDs
        test_id = str(uuid.uuid4())[:8]  # Use shorter UUID for readability
        agent = Agent(
            id=f"test-agent-{test_id}",
            name_str=f"Test Agent {test_id}",
            personality="Creative and insightful",
            art_style="impressionist",
            profile="Test agent profile",
            avatar="test_avatar.jpg",
            configs={},
            stats={},
            wallet_address=f"test-wallet-{test_id}",
            is_active=True
        )
        
        created_agent = agent_dao.create(agent)
        print(f"✅ Created agent: {created_agent.id}")

        # 2. Create mock NFT
        metadata = NFTMetadata(
            name=f"Test NFT {test_id}",
            description="A test NFT artwork",
            image_url="/path/to/image.jpg",
            art_style="impressionist",
            attributes={"test_attr": "test_value"},
            background_story="Test background story",
            creation_context="Test creation context"
        )
        
        nft = NFT(
            id=f"test-nft-{test_id}",
            token_id="",
            contract_address="",
            metadata=metadata,
            creator_id=created_agent.id,
            owner_id=created_agent.id,
            status=NFTStatus.DRAFT,
            created_at=datetime.utcnow()
        )
        
        created_nft = nft_dao.create(nft)
        print(f"✅ Created NFT: {created_nft.id}")

        # 3. Create mock critique
        critique = ArtworkCritique(
            id=f"test-critique-{test_id}",
            nft_id=created_nft.id,
            critic_agent_id=created_agent.id,
            critic_agent_name=created_agent.name_str,
            critique_details={
                "style_match": "Good match with impressionist style",
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
        
        created_critique = critique_dao.create(critique)
        print(f"✅ Created critique: {created_critique.id}")
        
        return created_agent.id, created_nft.id, created_critique.id
        
    except Exception as e:
        print(f"❌ Error creating test data: {str(e)}")
        return None, None, None

def check_tables():
    """Check if all required tables exist"""
    engine = create_engine(settings.DATABASE_URL)
    inspector = inspect(engine)
    
    required_tables = ['agent_tab', 'nft_tab', 'artwork_critique_tab']
    existing_tables = inspector.get_table_names()
    
    print("\n=== Table Check ===")
    for table in required_tables:
        exists = table in existing_tables
        print(f"Table {table}: {'✅' if exists else '❌'}")
    
    return all(table in existing_tables for table in required_tables)

def check_data():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Check Agents
        print("\n=== Agents ===")
        result = conn.execute(text("SELECT COUNT(*) FROM agent_tab"))
        count = result.scalar()
        print(f"Total Agents: {count}")
        
        result = conn.execute(text("""
            SELECT id, name, personality, is_active 
            FROM agent_tab 
            ORDER BY id
        """))
        
        print("\nAgents:")
        for row in result:
            print(f"ID: {row.id}")
            print(f"Name: {row.name}")
            print(f"Personality: {row.personality}")
            print(f"Active: {row.is_active}")
            print("---")

        # Check NFTs
        print("\n=== NFTs ===")
        result = conn.execute(text("SELECT COUNT(*) FROM nft_tab"))
        count = result.scalar()
        print(f"Total NFTs: {count}")
        
        result = conn.execute(text("""
            SELECT id, name, status, creator_id, created_at 
            FROM nft_tab 
            ORDER BY created_at DESC
        """))
        
        print("\nNFTs:")
        for row in result:
            print(f"ID: {row.id}")
            print(f"Name: {row.name}")
            print(f"Status: {row.status}")
            print(f"Creator: {row.creator_id}")
            print(f"Created: {row.created_at}")
            print("---")
            
        # Check Critiques
        print("\n=== Critiques ===")
        result = conn.execute(text("SELECT COUNT(*) FROM artwork_critique_tab"))
        count = result.scalar()
        print(f"Total Critiques: {count}")
        
        result = conn.execute(text("""
            SELECT id, nft_id, critic_agent_name, overall_score, created_at 
            FROM artwork_critique_tab 
            ORDER BY created_at DESC
        """))
        
        print("\nCritiques:")
        for row in result:
            print(f"ID: {row.id}")
            print(f"NFT ID: {row.nft_id}")
            print(f"Critic: {row.critic_agent_name}")
            print(f"Score: {row.overall_score}")
            print(f"Created: {row.created_at}")
            print("---")

def main():
    print("Initializing database...")
    if not check_tables():
        print("Creating tables...")
        init_db()
    
    print("\nSetting up test data...")
    agent_id, nft_id, critique_id = setup_test_data()
    
    if all([agent_id, nft_id, critique_id]):
        print("\nChecking database state...")
        check_data()
    else:
        print("Failed to set up test data")

if __name__ == "__main__":
    main()