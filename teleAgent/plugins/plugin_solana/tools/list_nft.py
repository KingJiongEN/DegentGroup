from typing import List, Optional, Dict, Any
from decimal import Decimal
import requests
from pydantic import BaseModel

class NFTListing(BaseModel):
    name: str
    price: Decimal
    seller: str
    image_url: str
    token_address: str
    mint_address: str

class NFTListingService:
    def __init__(self):
        self.base_url = "https://api-mainnet.magiceden.dev/v2"
        self.headers = {"accept": "application/json"}

    async def get_collection_listings(
        self, 
        collection_name: str,
        limit: int = 20
    ) -> List[NFTListing]:
        try:
            url = f"{self.base_url}/collections/{collection_name}/listings"
            response = requests.get(
                url,
                headers=self.headers,
                params={"limit": limit}
            )
            
            if response.status_code != 200:
                raise ConnectionError(f"API request failed: {response.status_code}")
                
            listings = response.json()
            return [
                NFTListing(
                    name=item["token"]["name"],
                    price=Decimal(str(item["price"])),
                    seller=item["seller"],
                    image_url=item["token"]["image"],
                    token_address=item["tokenAddress"],
                    mint_address=item["tokenMint"]
                )
                for item in listings
            ]

        except Exception as e:
            raise ConnectionError(f"Failed to fetch NFT listings: {str(e)}")

async def get_nft_listings(collection_name: str) -> List[Dict[str, Any]]:
    service = NFTListingService()
    listings = await service.get_collection_listings(collection_name)
    return [listing.dict() for listing in listings]