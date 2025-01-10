from typing import Protocol, Dict, Optional, List, Union
from dataclasses import dataclass
from decimal import Decimal

# Request Structures
@dataclass
class TotalValueRequest:
    """Request structure for total value query"""
    address: str
    chains: Union[str, List[str]]
    asset_type: Optional[str] = "0"  # "0": All, "1": Tokens only, "2": DeFi only
    exclude_risk_token: Optional[bool] = True

@dataclass
class TokenBalancesRequest:
    """Request structure for token balances query"""
    address: str
    chains: Union[str, List[str]]
    filter: Optional[str] = "0"  # Filter parameter for token balances

# Response Structures
@dataclass
class TotalValueResponse:
    """Response structure for total value query"""
    total_value: Decimal
    code: str
    message: str
    
    @classmethod
    def from_api_response(cls, response: Dict) -> 'TotalValueResponse':
        return cls(
            total_value=Decimal(response["data"][0]["totalValue"]) if response.get("data") else Decimal('0'),
            code=response.get("code", ""),
            message=response.get("msg", "")
        )

@dataclass
class TokenAsset:
    """Structure for individual token asset data"""
    chain_index: str
    token_address: str
    address: str
    symbol: str
    balance: Decimal
    token_price: Decimal
    token_type: str
    is_risk_token: bool
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TokenAsset':
        return cls(
            chain_index=data["chainIndex"],
            token_address=data["tokenAddress"],
            address=data["address"],
            symbol=data["symbol"],
            balance=Decimal(data["balance"]),
            token_price=Decimal(data["tokenPrice"]) if data["tokenPrice"] != "0" else Decimal('0'),
            token_type=data["tokenType"],
            is_risk_token=data["isRiskToken"]
        )

@dataclass
class TokenBalancesResponse:
    """Response structure for token balances query"""
    token_assets: List[TokenAsset]
    code: str
    message: str
    
    @classmethod
    def from_api_response(cls, response: Dict) -> 'TokenBalancesResponse':
        token_assets = []
        if response.get("code") == "0" and response.get("data"):
            for asset in response["data"][0].get("tokenAssets", []):
                token_assets.append(TokenAsset.from_dict(asset))
        
        return cls(
            token_assets=token_assets,
            code=response.get("code", ""),
            message=response.get("msg", "")
        )

class OKExClientInterface(Protocol):
    """Interface definition for OKEx API client"""
    
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        passphrase: str,
        project_id: Optional[str] = None,
        base_url: str = "https://www.okx.com",
        timeout: int = 30
    ) -> None: ...
    
    def get_total_value_by_address(
        self,
        request: TotalValueRequest
    ) -> TotalValueResponse: ...
    
    def get_all_token_balances_by_address(
        self,
        request: TokenBalancesRequest
    ) -> TokenBalancesResponse: ...
    
    def get(self, path: str, params: Optional[Dict] = None) -> Dict: ...
    
    def post(self, path: str, body: Optional[Dict] = None) -> Dict: ...