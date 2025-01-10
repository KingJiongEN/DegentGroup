from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Balance:
    """Represents a wallet's token balance"""

    amount: Decimal
    token_symbol: str
    wallet_address: str
    block_number: int = 0  # Latest block number when balance was fetched
    timestamp: int = 0  # Unix timestamp when balance was fetched
