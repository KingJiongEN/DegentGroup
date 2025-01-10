from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
import aiohttp
from solders.pubkey import Pubkey

from teleAgent.core.config import settings
from teleAgent.logger.logger import get_logger

from teleAgent.models.nft import NFTMetadata, NFTStatus, NFT
from teleAgent.plugins.plugin_solana.utils.image_gen import generate_image
from teleAgent.plugins.plugin_solana.utils.storage import upload_to_arweave


SYSTEM_PROGRAM_ID = Pubkey.from_string("11111111111111111111111111111111")
SYSVAR_RENT_PUBKEY = Pubkey.from_string("SysvarRent111111111111111111111111111111111")

logger = get_logger("plugin_solana:tools:create_nft")

@dataclass
class NFTCreationResult:
    success: bool
    token_id: Optional[str] = None
    image_url: Optional[str] = None
    metadata_url: Optional[str] = None
    tx_hash: Optional[str] = None
    error: Optional[str] = None
    nft: Optional[NFT] = None

async def create_nft_with_metadata(
    wallet_address: str,
    name: str,
    metadata_url: str,
    creator_id: str
) -> NFTCreationResult:
    if not metadata_url or not metadata_url.startswith('http'):
        return NFTCreationResult(
            success=False,
            error="Invalid metadata URL"
        )

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{settings.TOKEN_METADATA_SERVICE_URL}/api/nft/create",
                json={
                    "wallet_address": wallet_address,
                    "name": name,
                    "metadata_url": metadata_url,
                    "creator_id": creator_id
                }
            ) as response:
                result = await response.json()
                
                if not result["success"]:
                    return NFTCreationResult(
                        success=False,
                        error=result["error"]["message"]
                    )
                
                tx_hash = result["data"]["signature"]
                token_id = result["data"]["nft_address"]
                
                nft = NFT(
                    id=token_id,
                    token_id=token_id,
                    contract_address=settings.NFT_PROGRAM_ID,
                    metadata=None,
                    creator_id=creator_id,
                    owner_id=wallet_address,
                    status=NFTStatus.MINTED,
                    created_at=datetime.utcnow(),
                    minted_at=datetime.utcnow(),
                    transaction_hash=tx_hash
                )

                return NFTCreationResult(
                    success=True,
                    token_id=token_id,  
                    metadata_url=metadata_url,
                    tx_hash=tx_hash,
                    nft=nft
                )

        except aiohttp.ClientError as e:
            return NFTCreationResult(
                success=False,
                error=f"API request failed: {str(e)}"
            )

async def create_nft_with_generation(
    wallet_address: str,
    name: str,
    prompt: str,
    creator_id: str,
    style: str = None,
    metadata: Optional[NFTMetadata] = None
) -> NFTCreationResult:
    try:
        # Generate image
        image_data = await generate_image(prompt)
        if not image_data:
            raise Exception("Failed to generate image")
            
        # Upload image to Arweave
        image_url = await upload_to_arweave(image_data)
        logger.info(f"create_nft_with_generation image_url: {image_url}")

        # Create metadata
        nft_metadata = NFTMetadata(
            name=name,
            description=metadata.description if metadata else f"AI generated art: {prompt}",
            image_url=image_url,
            art_style=metadata.art_style if metadata else style,
            attributes={
                "style": metadata.art_style if metadata else style,
                "generation": 1,
                "prompt": prompt
            },
            creation_context=prompt
        )
        
        # Prepare metadata for Arweave
        metadata_json = {
            "name": nft_metadata.name,
            "symbol": "TRADE!",
            "description": nft_metadata.description,
            "image": nft_metadata.image_url,
            "attributes": [
                {"trait_type": k, "value": v}
                for k, v in nft_metadata.attributes.items()
            ]
        }
        
        # Upload metadata to Arweave
        metadata_url = await upload_to_arweave(metadata_json)
        logger.info(f"create_nft_with_generation metadata_url: {metadata_url}")

        # Create NFT
        result = await create_nft_with_metadata(
            wallet_address=wallet_address,
            name=name,
            metadata_url=metadata_url,
            creator_id=creator_id
        )
        
        if result.success and result.nft:
            result.nft.metadata = nft_metadata
            result.image_url = image_url

        return result

    except Exception as e:
        return NFTCreationResult(
            success=False,
            error=str(e)
        )