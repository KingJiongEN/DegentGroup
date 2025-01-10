from typing import List, Optional
from sqlalchemy.orm import sessionmaker

from teleAgent.database.tables.nft import NFTTable
from teleAgent.models.nft import NFT, NFTMetadata, NFTStatus
from .interface import INFTDAO

class NFTDAO(INFTDAO):
    def __init__(self, session_factory: sessionmaker):
        super().__init__(session_factory)

    def _to_model(self, table: NFTTable) -> NFT:
        metadata = NFTMetadata(
            name=table.name,
            description=table.description,
            image_url=table.image_path,
            art_style=table.art_style,
            attributes=table.attributes,
            background_story=table.background_story,
            creation_context=table.creation_context
        )
        
        return NFT(
            id=table.id,
            token_id=table.token_id,
            contract_address=table.contract_address,
            metadata=metadata,
            creator_id=table.creator_id,
            owner_id=table.current_owner_id,
            status=NFTStatus(table.status),
            created_at=table.created_at,
            minted_at=table.minted_at,
            chain_id=table.chain_id,
            transaction_hash=table.transaction_hash,
            mint_price=table.mint_price,
            last_transfer_at=table.last_transfer_at
        )

    def create(self, nft: NFT) -> NFT:
        with self._get_session() as session:
            table = NFTTable(
                id=nft.id,
                token_id=nft.token_id,
                contract_address=nft.contract_address,
                name=nft.metadata.name,
                description=nft.metadata.description,
                image_path=nft.metadata.image_url,
                art_style=nft.metadata.art_style,
                attributes=nft.metadata.attributes,
                background_story=nft.metadata.background_story,
                creation_context=nft.metadata.creation_context,
                creator_id=nft.creator_id,
                current_owner_id=nft.owner_id,
                status=nft.status.value,
                chain_id=nft.chain_id,
                transaction_hash=nft.transaction_hash,
                mint_price=nft.mint_price,
                minted_at=nft.minted_at,
                last_transfer_at=nft.last_transfer_at
            )
            session.add(table)
            session.flush()
            return self._to_model(table)

    def update(self, nft: NFT) -> Optional[NFT]:
        with self._get_session() as session:
            table = session.query(NFTTable).get(nft.id)
            if not table:
                return None
            
            # Update fields
            table.token_id = nft.token_id
            table.contract_address = nft.contract_address
            table.name = nft.metadata.name
            table.description = nft.metadata.description
            table.image_path = nft.metadata.image_url
            table.art_style = nft.metadata.art_style
            table.attributes = nft.metadata.attributes
            table.background_story = nft.metadata.background_story
            table.creation_context = nft.metadata.creation_context
            table.current_owner_id = nft.owner_id
            table.status = nft.status.value
            table.chain_id = nft.chain_id
            table.transaction_hash = nft.transaction_hash
            table.mint_price = nft.mint_price
            table.minted_at = nft.minted_at
            table.last_transfer_at = nft.last_transfer_at
            
            session.flush()
            return self._to_model(table)

    def delete(self, nft_id: str) -> bool:
        with self._get_session() as session:
            result = session.query(NFTTable).filter(NFTTable.id == nft_id).delete()
            return result > 0

    def get_by_id(self, nft_id: str) -> Optional[NFT]:
        with self._get_session() as session:
            table = session.query(NFTTable).get(nft_id)
            return self._to_model(table) if table else None

    def get_by_token_id(self, token_id: str) -> Optional[NFT]:
        with self._get_session() as session:
            table = session.query(NFTTable).filter(NFTTable.token_id == token_id).first()
            return self._to_model(table) if table else None

    def get_by_creator(self, creator_id: str) -> List[NFT]:
        with self._get_session() as session:
            tables = session.query(NFTTable).filter(NFTTable.creator_id == creator_id).all()
            return [self._to_model(t) for t in tables]

    def get_by_owner(self, owner_id: str) -> List[NFT]:
        with self._get_session() as session:
            tables = session.query(NFTTable).filter(NFTTable.current_owner_id == owner_id).all()
            return [self._to_model(t) for t in tables]

    def get_by_name(self, name: str) -> List[NFT]:
        """
        Retrieve NFTs by name.
        
        Args:
            name (str): The name of the NFT to search for
            
        Returns:
            List[NFT]: A list of NFTs matching the given name
        """
        with self._get_session() as session:
            tables = session.query(NFTTable).filter(NFTTable.name == name).all()
            return [self._to_model(t) for t in tables]
            