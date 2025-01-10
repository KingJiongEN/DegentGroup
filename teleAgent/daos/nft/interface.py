from abc import abstractmethod
from typing import List, Optional
from teleAgent.daos.base import BaseDAO
from teleAgent.models.nft import NFT
from teleAgent.database.tables.nft import NFTTable

class INFTDAO(BaseDAO[NFT, NFTTable]):
    @abstractmethod
    def _to_model(self, table: NFTTable) -> NFT:
        """Convert table entity to domain model"""
        pass

    @abstractmethod
    def create(self, nft: NFT) -> NFT:
        """Create a new NFT record"""
        pass

    @abstractmethod
    def update(self, nft: NFT) -> Optional[NFT]:
        """Update an existing NFT record"""
        pass

    @abstractmethod
    def delete(self, nft_id: str) -> bool:
        """Delete an NFT record by ID"""
        pass

    @abstractmethod
    def get_by_id(self, nft_id: str) -> Optional[NFT]:
        """Get an NFT by its ID"""
        pass

    @abstractmethod
    def get_by_creator(self, creator_id: str) -> List[NFT]:
        """Get all NFTs by creator ID"""
        pass

    @abstractmethod
    def get_by_owner(self, owner_id: str) -> List[NFT]:
        """Get all NFTs by owner ID"""
        pass