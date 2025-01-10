import pytest
from teleAgent.plugins.plugin_solana.tools.check_balance import check_wallet_balance_return_str

@pytest.mark.integration
class TestCheckWalletBalanceIntegration:
    # Well-known Solana addresses for testing
    TEST_WALLET = "CcRxmz35MtrweJWj4mF6cqaKHwh3actTbL2GtbChz6SJ"

    @pytest.mark.asyncio
    async def test_check_wallet_balance(self):
        """Test the check_wallet_balance function with a real wallet address."""
        try:
            balances_desc = await check_wallet_balance_return_str(self.TEST_WALLET)
            print(f"\ncheck_wallet_balance: {balances_desc}")
            assert isinstance(balances_desc, str)
        except ConnectionError as e:
            pytest.fail(f"Failed to check wallet balance: {str(e)}")
