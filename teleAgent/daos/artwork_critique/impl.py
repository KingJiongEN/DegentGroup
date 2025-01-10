from typing import List, Optional
from sqlalchemy.orm import sessionmaker

from teleAgent.database.tables.artwork_critique import ArtworkCritiqueTable
from teleAgent.models.artwork_critique import ArtworkCritique
from .interface import IArtworkCritiqueDAO

class ArtworkCritiqueDAO(IArtworkCritiqueDAO):
    def __init__(self, session_factory: sessionmaker):
        super().__init__(session_factory)
    
    def _to_model(self, table: ArtworkCritiqueTable) -> ArtworkCritique:
        return ArtworkCritique(
            id=table.id,
            nft_id=table.nft_id,
            critic_agent_id=table.critic_agent_id,
            critic_agent_name=table.critic_agent_name,
            critique_details=table.critique_details,
            overall_score=table.overall_score,
            created_at=table.created_at
        )
    
    def get_by_id(self, critique_id: str) -> Optional[ArtworkCritique]:
        with self._get_session() as session:
            table = session.query(ArtworkCritiqueTable).get(critique_id)
            return self._to_model(table) if table else None

    def create(self, critique: ArtworkCritique) -> ArtworkCritique:
        with self._get_session() as session:
            table = ArtworkCritiqueTable(
                id=critique.id,
                nft_id=critique.nft_id,
                critic_agent_id=critique.critic_agent_id,
                critic_agent_name=critique.critic_agent_name,
                critique_details=critique.critique_details,
                overall_score=critique.overall_score
            )
            session.add(table)
            session.flush()
            return self._to_model(table)

    def update(self, critique: ArtworkCritique) -> Optional[ArtworkCritique]:
        with self._get_session() as session:
            table = session.query(ArtworkCritiqueTable).get(critique.id)
            if not table:
                return None
            
            table.critique_details = critique.critique_details
            table.overall_score = critique.overall_score
            session.flush()
            return self._to_model(table)

    def delete(self, critique_id: str) -> bool:
        with self._get_session() as session:
            rows = session.query(ArtworkCritiqueTable)\
                .filter(ArtworkCritiqueTable.id == critique_id)\
                .delete()
            return rows > 0
    
    def get_by_nft_id(self, nft_id: str) -> List[ArtworkCritique]:
        with self._get_session() as session:
            tables = session.query(ArtworkCritiqueTable)\
                .filter(ArtworkCritiqueTable.nft_id == nft_id)\
                .all()
            return [self._to_model(t) for t in tables]
    
    def get_by_critic_id(self, critic_id: str) -> List[ArtworkCritique]:
        with self._get_session() as session:
            tables = session.query(ArtworkCritiqueTable)\
                .filter(ArtworkCritiqueTable.critic_agent_id == critic_id)\
                .all()
            return [self._to_model(t) for t in tables]
    
    def get_by_critic_nft_id(self, critic_id: str, nft_id: str) -> Optional[ArtworkCritique]:
        """
        Get a critique by both critic ID and NFT ID
        
        Args:
            critic_id: The ID of the critic agent
            nft_id: The ID of the NFT
            
        Returns:
            Optional[ArtworkCritique]: The critique if found, None otherwise
        """
        with self._get_session() as session:
            table = session.query(ArtworkCritiqueTable)\
                .filter(
                    ArtworkCritiqueTable.critic_agent_id == critic_id,
                    ArtworkCritiqueTable.nft_id == nft_id
                )\
                .first()
            return self._to_model(table) if table else None 