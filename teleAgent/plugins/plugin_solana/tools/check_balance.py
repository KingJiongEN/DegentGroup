from typing import Optional, Dict, Any
from decimal import Decimal

from teleAgent.core.config import settings
from teleAgent.plugins.plugin_solana.providers.wallet import WalletPortfolio, WalletProvider
from teleAgent.clients.okex.client import Client

def init_client() -> Client:
    """Create real OKEx client instance"""
    return Client(
        api_key=settings.OKEX_API_KEY,
        api_secret=settings.OKEX_API_SECRET,
        passphrase=settings.OKEX_PASSPHRASE,
        project_id=settings.OKEX_PROJECT_ID,
        base_url=settings.OKEX_BASE_URL
    )

async def check_wallet_balance(wallet_address: str) -> WalletPortfolio:
    try:
        okex_client = init_client()
        provider = WalletProvider(wallet_public_key=wallet_address, okex_client=okex_client)
        portfolio_value = await provider.fetch_portfolio_value()
        return portfolio_value

    except Exception as e:
        raise ConnectionError(f"Failed to fetch wallet balance: {str(e)}")

async def check_wallet_balance_return_str(wallet_address: str) -> str:
    try:
        okex_client = init_client()
        provider = WalletProvider(wallet_public_key=wallet_address, okex_client=okex_client)
        portfolio_desc = await provider.get_formatted_portfolio()
        return portfolio_desc

    except Exception as e:
        raise ConnectionError(f"Failed to fetch wallet balance: {str(e)}")
