from abc import abstractmethod
from typing import List, Optional
from teleAgent.daos.base import BaseDAO
from teleAgent.database.tables.artwork_critique import ArtworkCritiqueTable
from teleAgent.models.artwork_critique import ArtworkCritique

class IArtworkCritiqueDAO(BaseDAO[ArtworkCritique, ArtworkCritiqueTable]):
    """ArtworkCritique DAO Interface"""

    @abstractmethod
    def _to_model(self, table: ArtworkCritiqueTable) -> ArtworkCritique:
        """Convert table entity to domain model"""
        pass

    @abstractmethod
    def get_by_id(self, critique_id: str) -> Optional[ArtworkCritique]:
        """Get critique by ID"""
        pass

    @abstractmethod
    def create(self, critique: ArtworkCritique) -> ArtworkCritique:
        """Create new critique"""
        pass

    @abstractmethod
    def update(self, critique: ArtworkCritique) -> Optional[ArtworkCritique]:
        """Update existing critique"""
        pass

    @abstractmethod
    def delete(self, critique_id: str) -> bool:
        """Delete critique by ID"""
        pass

    @abstractmethod
    def get_by_nft_id(self, nft_id: str) -> List[ArtworkCritique]:
        """Get all critiques for an NFT"""
        pass

    @abstractmethod
    def get_by_critic_id(self, critic_id: str) -> List[ArtworkCritique]:
        """Get all critiques by a critic"""
        pass

    @abstractmethod
    def get_by_critic_nft_id(self, critic_id: str, nft_id: str) -> Optional[ArtworkCritique]:
        """Get critique by both critic ID and NFT ID"""
        pass