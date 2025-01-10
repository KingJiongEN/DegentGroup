from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from teleAgent.database.base import Base
from teleAgent.core.config import settings

# Import all models to ensure they are registered with Base
from teleAgent.database.tables.agent import AgentTable
from teleAgent.database.tables.dialog import DialogTable
from teleAgent.database.tables.memory import Memory
from teleAgent.database.tables.nft import NFTTable
from teleAgent.database.tables.twitter_auth import TwitterAuth
from teleAgent.database.tables.wallet import Wallet
from teleAgent.database.tables.post import Post
from teleAgent.database.tables.interaction import Interaction
from teleAgent.database.tables.user import User
from teleAgent.database.tables.artwork_critique import ArtworkCritiqueTable

def init_database():
    # Create engine
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=10
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    return engine, SessionLocal

if __name__ == "__main__":
    print("Initializing database...")
    engine, SessionLocal = init_database()
    print(f"Database initialized at: {settings.DATABASE_URL}") 