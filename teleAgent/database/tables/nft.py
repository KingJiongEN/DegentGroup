from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..base import Base


class NFTTable(Base):
    __tablename__ = "nft_tab"

    id = Column(String(100), primary_key=True, default=Base.generate_uuid)
    token_id = Column(String(100), nullable=True)  # On-chain token ID
    contract_address = Column(String(100), nullable=True)  # NFT contract address
    
    # Metadata fields
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    image_path = Column(String(500), nullable=False)
    art_style = Column(Text, nullable=False)
    attributes = Column(JSON, nullable=False, default=dict)
    background_story = Column(Text, nullable=True)
    creation_context = Column(Text, nullable=True)
    
    # Ownership and status
    creator_id = Column(String(100), ForeignKey('agent_tab.id'), nullable=False)
    current_owner_id = Column(String(100), ForeignKey('agent_tab.id'), nullable=False)
    status = Column(String(100), nullable=False, default='draft')
    
    # Blockchain info
    chain_id = Column(Float, nullable=True)
    transaction_hash = Column(String(100), nullable=True)
    mint_price = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    minted_at = Column(DateTime, nullable=True)
    last_transfer_at = Column(DateTime, nullable=True)

    # Relationships
    critiques = relationship("ArtworkCritiqueTable", back_populates="nft")

    def __repr__(self):
        return f"<NFT {self.name}>"