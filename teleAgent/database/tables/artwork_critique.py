from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..base import Base

class ArtworkCritiqueTable(Base):
    __tablename__ = 'artwork_critiques'
    
    id = Column(String(100), primary_key=True, default=Base.generate_uuid)
    nft_id = Column(String(100), ForeignKey('nft_tab.id'), nullable=False)
    critic_agent_id = Column(String(100), nullable=False)
    critic_agent_name = Column(String(100), nullable=False)
    critique_details = Column(JSON, nullable=False)  # Stores the detailed critique structure
    overall_score = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    nft = relationship("NFTTable", back_populates="critiques") 