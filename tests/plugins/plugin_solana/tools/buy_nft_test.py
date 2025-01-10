import pytest
from decimal import Decimal

from teleAgent.test.common import skip_in_github_actions
from teleAgent.plugins.plugin_solana.tools.buy_nft import buy_nft, NFTBuyingService
from teleAgent.logger.logger import get_logger
from teleAgent.core.config import settings

logger = get_logger('test.nft.buying')

@pytest.mark.integration
class TestBuyNFTIntegration:
    # Known Mad Lads NFT for testing
    TEST_NFT_MINT = "F361ngQ16WAzp6rmLZPFK72KmMmeiRe1SYsHMDdFPLLd"
    
    @classmethod
    def setup_class(cls):
        """Setup test environment"""
        pass

    @skip_in_github_actions
    @pytest.mark.asyncio 
    async def test_buy_specific_nft(self):
        """Test buying a specific NFT using known token_mint"""
        try:
            # Attempt to buy the NFT using METAPLEX_PRIVATE_KEY from settings
            result = await buy_nft(
                buyer_private_key=settings.METAPLEX_PRIVATE_KEY,
                token_mint=self.TEST_NFT_MINT
            )
            
            print(f"Transaction signature: {result}")
            
            assert result is not None
            logger.info(f"Successfully bought NFT {self.TEST_NFT_MINT}")
            logger.info(f"Transaction signature: {result}")
            
        except Exception as e:
            logger.red(f"Failed to buy NFT: {str(e)}")
            print("This test is for manual verification of specific NFT purchases")
            print("Failure may be expected if:")
            print("- The NFT is no longer listed")
            print("- The price has changed")
            print("- Insufficient funds in buyer wallet")
            print("- Network issues")
            raise

    @skip_in_github_actions
    @pytest.mark.asyncio 
    async def test_buy_core_mpl_nft(self):
        """Test buying a specific NFT using known token_mint"""
        try:
            test_nft_mint = "FJNkRAdc4aGQz6ngHGq7q82jp5XZEYCsg7TsUGEzzf79"

            # Attempt to buy the NFT using METAPLEX_PRIVATE_KEY from settings
            result = await buy_nft(
                buyer_private_key=settings.METAPLEX_PRIVATE_KEY,
                token_mint=test_nft_mint
            )
            
            print(f"Transaction signature: {result}")
            
            assert result is not None
            logger.info(f"Successfully bought NFT {test_nft_mint}")
            logger.info(f"Transaction signature: {result}")
            
        except Exception as e:
            logger.red(f"Failed to buy NFT: {str(e)}")
            print("This test is for manual verification of specific NFT purchases")
            print("Failure may be expected if:")
            print("- The NFT is no longer listed")
            print("- The price has changed")
            print("- Insufficient funds in buyer wallet")
            print("- Network issues")
            raise

    @skip_in_github_actions
    @pytest.mark.asyncio 
    async def test_buy_nft_error_handling(self):
        """Test error handling with invalid NFT mint"""
        try:
            invalid_mint = "InvalidMintAddress"
            
            with pytest.raises(Exception) as exc_info:
                await buy_nft(
                    buyer_private_key=settings.METAPLEX_PRIVATE_KEY,
                    token_mint=invalid_mint
                )
            
            assert exc_info.value is not None
            logger.info("Successfully caught error for invalid mint address")
            
        except Exception as e:
            logger.red(f"Unexpected error in error handling test: {str(e)}")
            raise

    async def helper_verify_nft_listing(self, token_mint: str) -> bool:
        """Helper method to verify if an NFT is listed and available"""
        try:
            service = NFTBuyingService()
            listing = await service.get_listing_info(token_mint)
            return listing is not None and listing.price > 0
        except Exception:
            return False