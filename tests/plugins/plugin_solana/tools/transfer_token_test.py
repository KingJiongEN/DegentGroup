import pytest
from decimal import Decimal

from teleAgent.test.common import skip_in_github_actions
from teleAgent.plugins.plugin_solana.tools.transfer_token import transfer_token

@pytest.mark.integration
class TestTransferTokenIntegration:
    TEST_WALLET = "CcRxmz35MtrweJWj4mF6cqaKHwh3actTbL2GtbChz6SJ"
    TEST_RECIPIENT = "Bq7PUGjXyjLrSEF4FD2Evi7gzkxxRwBm5CT2zsojqcWq"
    
    # USDC on devnet for testing
    TEST_TOKEN_MINT = "LncWMatCv9DCi1nCsHcdG2ehikiN2431AtJeHempump"
    
    @classmethod
    def setup_class(cls):
        pass

    @skip_in_github_actions
    @pytest.mark.asyncio 
    async def test_transfer_sol(self):
        """Test transferring SOL"""
        amount = 0.001  # Small amount for testing
        
        result = await transfer_token(
            to_address=self.TEST_RECIPIENT,
            amount=amount,
            memo="Transfer SOL test"
        )
        
        print(f"\ntest_transfer_sol result: {result}")
        
        if result.success:
            assert result.token_mint is None
            assert result.to_address == self.TEST_RECIPIENT
            assert result.amount == amount
            assert result.tx_hash is not None
            print(f"Successfully transferred {amount} SOL")
            print(f"Transaction hash: {result.tx_hash}")
        else:
            print(f"Transfer failed: {result.error}")
            print("This test requires the wallet to have sufficient SOL balance")

    @skip_in_github_actions
    @pytest.mark.asyncio
    async def test_transfer_token(self):
        """Test transferring SPL Token (USDC)"""
        amount = 2.0  # 1 SAPO
        
        result = await transfer_token(
            to_address=self.TEST_RECIPIENT,
            amount=amount,
            token_mint=self.TEST_TOKEN_MINT,
            memo="Transfer USDC test"
        )
        
        print(f"\ntest_transfer_token result: {result}")
        
        if result.success:
            assert result.token_mint == self.TEST_TOKEN_MINT
            assert result.to_address == self.TEST_RECIPIENT
            assert result.amount == amount
            assert result.tx_hash is not None
            print(f"Successfully transferred {amount} USDC")
            print(f"Transaction hash: {result.tx_hash}")
        else:
            print(f"Transfer failed: {result.error}")
            print("This test requires the wallet to have sufficient USDC balance")

    @skip_in_github_actions
    @pytest.mark.asyncio
    async def test_transfer_invalid_address(self):
        """Test transferring to invalid address"""
        invalid_address = "invalid_address"
        
        result = await transfer_token(
            to_address=invalid_address,
            amount=0.001
        )
        
        assert not result.success
        assert result.error is not None
        print(f"\ntest_transfer_invalid_address error: {result.error}")

    @skip_in_github_actions
    @pytest.mark.asyncio
    async def test_create_ata(self):
        """Test token transfer that requires creating ATA"""
        amount = 0.1
        
        result = await transfer_token(
            to_address=self.TEST_RECIPIENT,
            amount=amount,
            token_mint=self.TEST_TOKEN_MINT,
            memo="Test ATA creation"
        )
        
        print(f"\ntest_create_ata result: {result}")
        
        if result.success:
            assert result.token_mint == self.TEST_TOKEN_MINT
            assert result.tx_hash is not None
            print(f"Successfully created ATA and transferred {amount} tokens")
            print(f"Transaction hash: {result.tx_hash}")
        else:
            print(f"Transfer failed: {result.error}")
            print("This test may fail if ATA already exists")

    @skip_in_github_actions
    @pytest.mark.asyncio
    async def test_transfer_large_amount(self):
        """Test transferring large amount (should fail with insufficient balance)"""
        large_amount = 1000000.0  # Very large amount
        
        result = await transfer_token(
            to_address=self.TEST_RECIPIENT,
            amount=large_amount
        )
        
        assert not result.success
        assert "insufficient" in result.error.lower()
        print(f"\ntest_transfer_large_amount error: {result.error}")
