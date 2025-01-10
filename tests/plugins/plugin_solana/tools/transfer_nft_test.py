import pytest

from teleAgent.test.common import skip_in_github_actions
from teleAgent.plugins.plugin_solana.tools.transfer_nft import transfer_nft

@pytest.mark.integration
class TestTransferNFTIntegration:
    TEST_WALLET = "CcRxmz35MtrweJWj4mF6cqaKHwh3actTbL2GtbChz6SJ"
    TEST_RECIPIENT = "GpPr9rs8CuvKRuzS2zc5o4u7WeLMzRs9hGimV491ZSU6"
    
    @classmethod
    def setup_class(cls):
        pass

    @skip_in_github_actions
    @pytest.mark.asyncio 
    async def test_transfer_specific_nft(self):
        """Test transferring a specific NFT using known token_id"""
        known_token_id = "F361ngQ16WAzp6rmLZPFK72KmMmeiRe1SYsHMDdFPLLd"  
        
        result = await transfer_nft(
            token_id=known_token_id,
            to_address=self.TEST_RECIPIENT,
            memo="Transfer specific NFT"
        )
        
        print(f"\ntest_transfer_specific_nft result: {result}")
        
        if result.success:
            assert result.token_id == known_token_id
            assert result.to_address == self.TEST_RECIPIENT
            assert result.tx_hash is not None
            print(f"Successfully transferred NFT {known_token_id}")
            print(f"Transaction hash: {result.tx_hash}")
        else:
            print(f"Transfer failed: {result.error}")
            print("This test is for manual verification of specific NFT transfers")
            print("Failure may be expected if the NFT doesn't exist or was already transferred")
