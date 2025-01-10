import pytest
from decimal import Decimal

from teleAgent.clients.okex.client import Client
from teleAgent.clients.okex.interface import (
    TotalValueRequest,
    TotalValueResponse,
    TokenBalancesRequest,
    TokenBalancesResponse,
    TokenAsset
)
from teleAgent.core.config import settings

@pytest.fixture
def okex_client() -> Client:
    """Create an OKEx client instance with real credentials."""
    return Client(
        api_key=settings.OKEX_API_KEY,
        api_secret=settings.OKEX_API_SECRET,
        passphrase=settings.OKEX_PASSPHRASE,
        project_id=settings.OKEX_PROJECT_ID,
        base_url=settings.OKEX_BASE_URL
    )

@pytest.fixture
def test_address() -> str:
    """Return a test address known to have assets."""
    return "FpxqiqSUdpkvNNDBEjUYtynqELmAu8q5VtmgJ7VZ9ehW" 

@pytest.mark.integration
def test_get_total_value(okex_client: Client, test_address: str) -> None:
    """Test getting total value for a known address on Ethereum mainnet."""
    request = TotalValueRequest(
        address=test_address,
        chains="501",  # Ethereum mainnet
        asset_type="0",  # All assets
        exclude_risk_token=True
    )
    
    response = okex_client.get_total_value_by_address(request)
    
    # Verify response structure and types
    assert isinstance(response, TotalValueResponse)
    assert isinstance(response.total_value, Decimal)
    assert response.code == "0"  # Successful response
    assert response.total_value >= 0
    
    print(f"\nTotal value for {test_address}: ${response.total_value:f} USD")
    print(f"Response code: {response.code}")
    print(f"Response message: {response.message}")

@pytest.mark.integration
def test_get_all_token_balances(okex_client: Client, test_address: str) -> None:
    """Test getting all token balances for a known address on Ethereum."""
    request = TokenBalancesRequest(
        address=test_address,
        chains="501",  # Ethereum mainnet
        filter="1"  # Filter out risk tokens
    )
    
    response = okex_client.get_all_token_balances_by_address(request)
    
    # Verify response structure
    assert isinstance(response, TokenBalancesResponse)
    assert isinstance(response.token_assets, list)
    assert response.code == "0"  # Successful response
    
    if response.token_assets:  # If address has tokens
        token = response.token_assets[0]
        # Verify token asset structure and types
        assert isinstance(token, TokenAsset)
        assert isinstance(token.chain_index, str)
        assert isinstance(token.token_address, str)
        assert isinstance(token.address, str)
        assert isinstance(token.symbol, str)
        assert isinstance(token.balance, Decimal)
        assert isinstance(token.token_price, Decimal)
        assert isinstance(token.token_type, str)
        assert isinstance(token.is_risk_token, bool)
        
        print(f"\nFound {len(response.token_assets)} tokens for {test_address}")
        print(f"First token details:")
        print(f"  Symbol: {token.symbol}")
        print(f"  Balance: {token.balance}")
        print(f"  Price: ${token.token_price}")
        print(f"  Chain Index: {token.chain_index}")
        print(f"  Token Address: {token.token_address}")
        print(f"  Token Type: {token.token_type}")
        print(f"  Is Risk Token: {token.is_risk_token}")
        print(f"Response code: {response.code}")
        print(f"Response message: {response.message}")
