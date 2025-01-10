import pytest
from teleAgent.plugins.plugin_solana.providers.wallet import WalletProvider
from teleAgent.clients.okex.client import Client
from teleAgent.core.config import settings

@pytest.mark.integration
class TestWalletProviderIntegration:
    # Well-known Solana addresses for testing
    TEST_ADDRESSE = "FpxqiqSUdpkvNNDBEjUYtynqELmAu8q5VtmgJ7VZ9ehW"
    
    RETRY_COUNT = 3
    RETRY_DELAY = 2  # seconds

    @pytest.fixture(scope="class")
    def okex_client(self):
        """Create real OKEx client instance"""
        if not all([
            settings.OKEX_API_KEY,
            settings.OKEX_API_SECRET,
            settings.OKEX_PASSPHRASE
        ]):
            pytest.skip("OKEx credentials not configured")
            
        return Client(
            api_key=settings.OKEX_API_KEY,
            api_secret=settings.OKEX_API_SECRET,
            passphrase=settings.OKEX_PASSPHRASE,
            project_id=settings.OKEX_PROJECT_ID,
            base_url=settings.OKEX_BASE_URL
        )

    @pytest.fixture()
    def wallet_provider(self, okex_client):
        """Create WalletProvider instance with different test addresses"""
        return WalletProvider(
            wallet_public_key=self.TEST_ADDRESSE,
            okex_client=okex_client
        )

    @pytest.mark.asyncio
    async def test_formatted_portfolio(self, wallet_provider):
        """Test portfolio formatting with real data"""
        formatted_result = await wallet_provider.get_formatted_portfolio()

        # Verify formatting
        assert isinstance(formatted_result, str)
        assert wallet_provider.wallet_public_key in formatted_result
        assert "Total Value: $" in formatted_result
        assert "Token Balances:" in formatted_result

        # Print results for manual verification
        print(f"\nFormatted Portfolio for {wallet_provider.wallet_public_key}:")
        print(formatted_result)