import pytest
from teleAgent.plugins.plugin_solana.tools.list_nft import get_nft_listings

@pytest.mark.integration
class TestNFTListingsIntegration:
    # Well-known collection for testing
    TEST_COLLECTION = "mad_lads"

    @pytest.mark.asyncio
    async def test_get_nft_listings(self):
        """Test the get_nft_listings function with a real collection."""
        try:
            listings = await get_nft_listings(self.TEST_COLLECTION)
            print(f"\nget_nft_listings: {listings[:2]}")  # Print first 2 listings for review
            
            assert isinstance(listings, list)
            assert len(listings) > 0
            
            # Verify structure of first listing
            first_listing = listings[0]
            assert "name" in first_listing
            assert "price" in first_listing
            assert "seller" in first_listing
            assert "image_url" in first_listing
            assert "token_address" in first_listing
            assert "mint_address" in first_listing
            
        except ConnectionError as e:
            pytest.fail(f"Failed to fetch NFT listings: {str(e)}")