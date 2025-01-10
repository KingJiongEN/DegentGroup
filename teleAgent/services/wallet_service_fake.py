from decimal import Decimal
from typing import Dict

from teleAgent.models.wallet import Balance
from teleAgent.services.interfaces import IWalletService


class WalletServiceFake(IWalletService):
    def __init__(self):
        # Mock wallet storage for testing
        self._wallets: Dict[str, Decimal] = {}
        self._default_token = "SOL"

    async def get_balance(self, wallet_address: str) -> Balance:
        """Get wallet balance"""
        # Return 0 if wallet doesn't exist
        amount = self._wallets.get(wallet_address, Decimal("0.0"))
        return Balance(
            amount=amount,
            token_symbol=self._default_token,
            wallet_address=wallet_address,
            block_number=1,  # Mock block number
            timestamp=1234567890,  # Mock timestamp
        )

    async def transfer(self, from_address: str, to_address: str, amount: float) -> bool:
        """Transfer tokens between wallets"""
        amount_decimal = Decimal(str(amount))

        # Check if sender has enough balance
        if self._wallets.get(from_address, Decimal("0.0")) < amount_decimal:
            return False

        # Update balances
        self._wallets[from_address] = (
            self._wallets.get(from_address, Decimal("0.0")) - amount_decimal
        )
        self._wallets[to_address] = (
            self._wallets.get(to_address, Decimal("0.0")) + amount_decimal
        )

        return True

    async def create_wallet(self) -> str:
        """Create new wallet and return address"""
        # Generate mock wallet address
        import uuid

        wallet_address = f"mock_{uuid.uuid4().hex[:10]}"

        # Initialize wallet with 0 balance
        self._wallets[wallet_address] = Decimal("0.0")

        return wallet_address

    # Helper methods for testing
    async def _mock_fund_wallet(self, wallet_address: str, amount: float) -> None:
        """Add funds to wallet (for testing)"""
        self._wallets[wallet_address] = Decimal(str(amount))

    async def _mock_reset(self) -> None:
        """Reset all wallets (for testing)"""
        self._wallets.clear()
