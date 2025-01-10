from dataclasses import dataclass
from typing import List, Dict, Optional
from decimal import Decimal
import traceback
import aiohttp
import asyncio
from teleAgent.clients.okex.interface import (
    OKExClientInterface,
    TokenBalancesRequest,
    TotalValueRequest
)
from teleAgent.core.config import settings
from teleAgent.logger.logger import get_logger
from arweave.arweave_lib import Wallet
from tenacity import retry, wait_exponential, stop_after_attempt
from teleAgent.plugins.plugin_solana.utils.arweave.check_balance import ArweaveBalance, WalletBalance

logger = get_logger("plugin_solana:providers:wallet")

@dataclass
class Item:
    name: str 
    address: str
    symbol: str
    balance: str
    ui_amount: str  
    price_usd: str
    value_usd: str
    value_sol: str = None

@dataclass
class NFTItem:
    token_id: str
    collection: str
    metadata: Dict
    floor_price: Optional[float] = None

@dataclass
class WalletPortfolio:
    total_usd: str
    total_sol: str
    items: List[Item]
    nfts: List[NFTItem]
    ar_balance: Optional[WalletBalance] = None

class WalletProvider:
    SUPPORTED_CHAINS = ["501"]  # Can be extended for other chains

    def __init__(self, wallet_public_key: str, okex_client: Optional[OKExClientInterface] = None):
        self.wallet_public_key = wallet_public_key
        self.okex_client = okex_client or self._create_default_client()
        self.metadata_url = f"{settings.TOKEN_METADATA_SERVICE_URL}/api/nft/owner"
        self.ar_checker = ArweaveBalance()

    def _create_default_client(self) -> OKExClientInterface:
        return OKExClientInterface(
            api_key=settings.OKEX_API_KEY,
            api_secret=settings.OKEX_API_SECRET,
            passphrase=settings.OKEX_PASSPHRASE
        )

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    async def _fetch_nfts(self) -> List[NFTItem]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.metadata_url}/{self.wallet_public_key}",
                    timeout=settings.TOKEN_METADATA_SERVICE_TIMEOUT
                ) as resp:
                    if resp.status != 200:
                        raise Exception(f"NFT fetch failed with status {resp.status}")
                    
                    data = await resp.json()
                    logger.debug(f"_fetch_nfts data: {data}", extra={"request_url": self.metadata_url, "wallet_public_key": self.wallet_public_key})

                    if not data.get("success"):
                        raise Exception(data.get("error", {}).get("message", "Unknown error"))

                    nfts = []
                    for token in data["data"]["tokens"]:
                        nft = NFTItem(
                            token_id=token["mint"],
                            collection="",
                            metadata=token["metadata"],
                            floor_price=None
                        )
                        nfts.append(nft)
                    return nfts
                    
        except asyncio.TimeoutError:
            raise Exception("NFT fetch timeout")
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"Error transferring NFT:\n{error_trace}")
            raise Exception(f"Failed to fetch NFTs: {str(e)}")

    async def _fetch_ar_balance(self) -> Optional[WalletBalance]:
        try:
            wallet = Wallet(settings.ARWEAVE_JWK_FILE)
            return self.ar_checker.check_by_address(wallet.address)
        except Exception as e:
            logger.error(f"Failed to fetch AR balance: {str(e)}")
            return None
        
    async def fetch_portfolio_value(self) -> WalletPortfolio:
        try:
            total_value_req = TotalValueRequest(
                address=self.wallet_public_key,
                chains=self.SUPPORTED_CHAINS
            )
            
            balances_req = TokenBalancesRequest(
                address=self.wallet_public_key,
                chains=self.SUPPORTED_CHAINS
            )

            total_value_resp = self.okex_client.get_total_value_by_address(total_value_req)
            logger.debug(f"fetch_portfolio_value total_value_resp: {total_value_resp}") 

            balances_resp = self.okex_client.get_all_token_balances_by_address(balances_req)
            logger.debug(f"fetch_portfolio_value balances_resp: {balances_resp}") 

            ar_balance = await self._fetch_ar_balance()
            total_value = Decimal(total_value_resp.total_value)
            
            if ar_balance and ar_balance.value_usd:
                total_value += Decimal(str(ar_balance.value_usd))

            items = []
            for token in balances_resp.token_assets:
                value_usd = token.balance * token.token_price
                item = Item(
                    name=token.symbol,
                    address=token.token_address,
                    symbol=token.symbol,
                    balance=str(token.balance),
                    ui_amount=str(token.balance),
                    price_usd=str(token.token_price),
                    value_usd=str(value_usd),
                    value_sol=self._calculate_sol_value(value_usd, balances_resp)
                )
                items.append(item)

            items.sort(key=lambda x: Decimal(x.value_usd), reverse=True)

            nfts = await self._fetch_nfts()

            return WalletPortfolio(
                total_usd=str(total_value_resp.total_value),
                total_sol=self._calculate_total_sol_value(total_value_resp.total_value, balances_resp),
                items=items,
                nfts=nfts,
                ar_balance=ar_balance
            )

        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"Error fetching portfolio:\n{error_trace}")
            raise Exception(f"Error fetching portfolio: {str(e)}")

    def _calculate_sol_value(self, value_usd: Decimal, balances_resp) -> str:
        sol_token = next(
            (token for token in balances_resp.token_assets if token.symbol == "SOL"),
            None
        )
        if sol_token and sol_token.token_price:
            return str(value_usd / sol_token.token_price)
        return "0"

    def _calculate_total_sol_value(self, total_usd: Decimal, balances_resp) -> str:
        sol_token = next(
            (token for token in balances_resp.token_assets if token.symbol == "SOL"),
            None
        )
        if sol_token and sol_token.token_price:
            return str(total_usd / sol_token.token_price)
        return "0"

    async def get_formatted_portfolio(self) -> str:
        try:
            portfolio = await self.fetch_portfolio_value()
            
            output = [
                f"Wallet Address: {self.wallet_public_key}\n",
                f"Total Value: ${float(portfolio.total_usd):.6f} ({float(portfolio.total_sol):.6f} SOL)\n",
            ]

            if portfolio.ar_balance:
                output.extend([
                    f"AR Address: {portfolio.ar_balance.address}",
                    f"Arweave Balance:",
                    f"AR: {portfolio.ar_balance.balance_ar:.6f}",
                    f"Value: ${portfolio.ar_balance.value_usd:.2f}\n"
                ])

            output.append("Token Balances:")
            non_zero_items = [item for item in portfolio.items if Decimal(item.ui_amount) > 0]

            if not non_zero_items:
                output.append("No tokens found with non-zero balance")
            else:
                for item in non_zero_items:
                    output.append(
                        f"{item.symbol} ({item.address}): {float(item.ui_amount):.6f} "
                        f"(${float(item.value_usd):.6f} | {float(item.value_sol):.6f} SOL)"
                    )

            if portfolio.nfts:
                output.append("\nNFT Collection:")
                for nft in portfolio.nfts:
                    output.append(
                        f"{nft.metadata.get('name', 'Unnamed')} "
                        f"(TokenID: {nft.token_id})"
                        f"(URI: {nft.metadata.get('uri', '')})"
                    )
            else:
                output.append("\nNo NFTs found")

            return "\n".join(output)
            
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"Error transferring NFT:\n{error_trace}")
            return f"Unable to fetch wallet information: {str(e)}"
