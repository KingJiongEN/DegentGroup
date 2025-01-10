import pytest
from teleAgent.test.common import skip_in_github_actions
from teleAgent.plugins.plugin_solana.tools.create_nft import (
    create_nft_with_metadata,
    create_nft_with_generation as create_nft,
    NFTCreationResult
)
from teleAgent.models.nft import  NFTMetadata
from teleAgent.core.config import settings

@pytest.mark.integration
class TestCreateNFTIntegration:
    TEST_WALLET = "CcRxmz35MtrweJWj4mF6cqaKHwh3actTbL2GtbChz6SJ"
    
    @classmethod
    def setup_class(cls):
        # 如果需要在所有测试前运行一次的设置代码
        pass

    @skip_in_github_actions
    @pytest.mark.asyncio
    async def test_create_nft_with_metadata_success(self):
        """Test successful NFT creation with minimal parameters"""
        result = await create_nft_with_metadata(
            wallet_address=self.TEST_WALLET,
            name="Test NFT",
            metadata_url="https://arweave.net/KMqr5IowiHhfxhd_Yo1y6tnF2cc6sryeD3cU9IIxpFk",
            creator_id=self.TEST_WALLET
        )
        
        print(f"\ntest_create_nft_with_metadata_success result: {result}")

        assert isinstance(result, NFTCreationResult)
        assert result.success is True
        assert result.token_id is not None
        assert result.metadata_url is not None
        assert result.tx_hash is not None
        assert result.error is None
        assert result.nft is not None

    @skip_in_github_actions
    @pytest.mark.asyncio
    async def test_create_nft_success(self):
        """Test successful NFT creation with minimal parameters"""
        result = await create_nft(
            wallet_address=self.TEST_WALLET,
            name="Test NFT",
            prompt="A beautiful sunset over mountains",
            creator_id=self.TEST_WALLET
        )
        
        assert isinstance(result, NFTCreationResult)
        assert result.success is True
        assert result.token_id is not None
        assert result.image_url is not None
        assert result.metadata_url is not None
        assert result.tx_hash is not None
        assert result.nft is not None

    @skip_in_github_actions
    @pytest.mark.asyncio
    async def test_create_nft_with_style(self):
        """Test NFT creation with specific art style"""
        result = await create_nft(
            wallet_address=self.TEST_WALLET,
            name="Futuristic Test NFT",
            prompt="A cyberpunk city at night",
            creator_id=self.TEST_WALLET,
            style="futurism"
        )
        
        assert result.success is True
        assert result.nft is not None
        assert result.nft.metadata.art_style == "futurism"

    @skip_in_github_actions
    @pytest.mark.asyncio
    async def test_create_nft_with_metadata(self):
        """Test NFT creation with custom metadata"""
        metadata = NFTMetadata(
            name="Custom NFT",
            description="Custom NFT description",
            image_url="",
            art_style="abstract",
            attributes={
                "artist": "TestArtist",
                "rarity": "rare",
                "edition": 1
            }
        )
        
        result = await create_nft(
            wallet_address=self.TEST_WALLET,
            name="Metadata Test NFT",
            prompt="Abstract geometric shapes",
            creator_id=self.TEST_WALLET,
            metadata=metadata
        )
        
        assert result.success is True
        assert result.nft is not None
        assert result.nft.metadata.attributes["artist"] == "TestArtist"

    @skip_in_github_actions
    @pytest.mark.asyncio
    async def test_create_nft_invalid_wallet(self):
        """Test NFT creation with invalid wallet address"""
        result = await create_nft(
            wallet_address="invalid_address",
            name="Failed NFT",
            prompt="This should fail",
            creator_id=self.TEST_WALLET
        )
        
        assert result.success is False
        assert result.error is not None

    @skip_in_github_actions
    @pytest.mark.asyncio
    async def test_create_nft_empty_prompt(self):
        """Test NFT creation with empty prompt"""
        result = await create_nft(
            wallet_address=self.TEST_WALLET,
            name="Empty Prompt NFT",
            prompt="",
            creator_id=self.TEST_WALLET
        )
        
        assert result.success is False
        assert result.error is not None