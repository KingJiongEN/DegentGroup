import uuid
from datetime import datetime
from typing import Dict, List, Optional

from teleAgent.models.nft import NFT
from teleAgent.services.interfaces import INFTService


class NFTServiceFake(INFTService):
    def __init__(self):
        # Mock storage for NFTs
        self._nfts: Dict[str, NFT] = {}
        self._ownership: Dict[str, str] = {}  # nft_id -> owner_id mapping

    async def get_latest_mints(self, limit: int = 5) -> List[NFT]:
        """Get most recently minted NFTs"""
        # Sort NFTs by creation time and return latest ones
        sorted_nfts = sorted(
            self._nfts.values(), key=lambda x: x.created_at, reverse=True
        )
        return sorted_nfts[:limit]

    async def get_agent_nfts(self, agent_id: str) -> List[NFT]:
        """Get NFTs owned by an agent"""
        return [
            nft
            for nft_id, nft in self._nfts.items()
            if self._ownership.get(nft_id) == agent_id
        ]

    async def mint(self, creator_id: str, metadata: Dict) -> NFT:
        """Mint new NFT"""
        nft_id = str(uuid.uuid4())

        nft = NFT(
            id=nft_id,
            creator_id=creator_id,
            metadata=metadata,
            token_id=f"MOCK_TOKEN_{nft_id[:8]}",
            contract_address=f"MOCK_CONTRACT_{uuid.uuid4().hex[:10]}",
            created_at=datetime.utcnow(),
            transaction_hash=f"MOCK_TX_{uuid.uuid4().hex}",
        )

        self._nfts[nft_id] = nft
        self._ownership[nft_id] = creator_id

        return nft

    async def transfer_nft(self, nft_id: str, from_id: str, to_id: str) -> bool:
        """Transfer NFT ownership"""
        # Verify NFT exists and sender owns it
        if nft_id not in self._nfts or self._ownership.get(nft_id) != from_id:
            return False

        # Update ownership
        self._ownership[nft_id] = to_id
        return True

    # Helper methods for testing
    async def _mock_reset(self) -> None:
        """Reset all NFTs and ownership data (for testing)"""
        self._nfts.clear()
        self._ownership.clear()

    async def _mock_get_owner(self, nft_id: str) -> Optional[str]:
        """Get current owner of NFT (for testing)"""
        return self._ownership.get(nft_id)

    async def _mock_add_nft(self, nft: NFT, owner_id: str) -> None:
        """Directly add NFT to storage (for testing)"""
        self._nfts[nft.id] = nft
        self._ownership[nft.id] = owner_id
