from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional


class NFTStatus(Enum):
    """Status of an NFT"""

    DRAFT = "draft"  # Being created
    MINTING = "minting"  # In minting process
    MINTED = "minted"  # Successfully minted
    TRANSFERRING = "transferring"  # Being transferred
    BURNED = "burned"  # Burned/destroyed


@dataclass
class NFTMetadata:
    """Metadata for an NFT"""

    name: str
    description: str
    image_url: str
    art_style: str
    attributes: Dict[str, Any]
    external_url: Optional[str] = None
    background_story: Optional[str] = None
    creation_context: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert NFTMetadata to a dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "image_url": self.image_url,
            "art_style": self.art_style,
            "attributes": self.attributes,
        }


@dataclass
class NFT:
    """Represents an NFT in the system"""

    id: str
    token_id: str  # On-chain token ID
    contract_address: str  # NFT contract address
    metadata: NFTMetadata
    creator_id: str  # Agent ID who created it
    owner_id: str  # Current owner's Agent ID
    status: NFTStatus
    created_at: datetime
    minted_at: Optional[datetime] = None

    chain_id: int = 1  # Blockchain network ID
    transaction_hash: Optional[str] = None
    mint_price: Optional[Decimal] = None
    last_transfer_at: Optional[datetime] = None

    def is_minted(self) -> bool:
        """Check if NFT is minted"""
        return self.status == NFTStatus.MINTED

    def is_owned_by(self, agent_id: str) -> bool:
        """Check if NFT is owned by specified agent"""
        return self.owner_id == agent_id

    def can_transfer(self) -> bool:
        """Check if NFT can be transferred"""
        return self.is_minted() and self.status != NFTStatus.TRANSFERRING


@dataclass
class NFTTransfer:
    """Records an NFT transfer"""

    id: str
    nft_id: str
    from_agent_id: str
    to_agent_id: str
    transaction_hash: str
    timestamp: datetime
    status: str
    reason: Optional[str] = None  # Why the transfer happened
    emotion_trigger: Optional[str] = None  # What emotion triggered transfer
