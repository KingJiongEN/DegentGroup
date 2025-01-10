from typing import Dict, Optional, List, Union
import hmac
import base64
import json
from datetime import datetime
import requests

from .interface import (
    OKExClientInterface,
    TotalValueRequest,
    TotalValueResponse,
    TokenBalancesRequest,
    TokenBalancesResponse
)

class Client(OKExClientInterface):
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        passphrase: str,
        project_id: Optional[str] = None,
        base_url: str = "https://www.okx.com",
        timeout: int = 30
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.project_id = project_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def _get_timestamp(self) -> str:
        """Generate ISO format timestamp."""
        return datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'

    def _sign(self, timestamp: str, method: str, request_path: str, body: str = '') -> str:
        """
        Generate HMAC SHA256 signature.
        :param timestamp: ISO format timestamp
        :param method: HTTP method (GET, POST, etc.)
        :param request_path: API endpoint path
        :param body: Request body for POST requests
        :return: Base64 encoded signature
        """
        message = timestamp + method + request_path + body
        mac = hmac.new(
            bytes(self.api_secret, encoding='utf8'),
            bytes(message, encoding='utf-8'),
            digestmod='sha256'
        )
        return base64.b64encode(mac.digest()).decode()

    def _build_headers(self, method: str, request_path: str, body: str = '') -> Dict:
        """Build headers with authentication info."""
        timestamp = self._get_timestamp()
        sign = self._sign(timestamp, method, request_path, body)
        
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': sign,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        
        if self.project_id:
            headers['OK-ACCESS-PROJECT'] = self.project_id
            
        return headers

    def _request(self, method: str, path: str, params: Optional[Dict] = None, body: Optional[Dict] = None) -> Dict:
        """Send HTTP request to OKEx API."""
        url = self.base_url + path
        
        if params:
            query_string = '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
            sign_path = path + query_string
        else:
            sign_path = path
            
        body_str = json.dumps(body) if body else ''
        headers = self._build_headers(method, sign_path, body_str)
        
        response = requests.request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            json=body if body else None,
            timeout=self.timeout
        )
        
        response.raise_for_status()
        return response.json()

    def get(self, path: str, params: Optional[Dict] = None) -> Dict:
        """Send GET request."""
        return self._request('GET', path, params=params)

    def post(self, path: str, body: Optional[Dict] = None) -> Dict:
        """Send POST request."""
        return self._request('POST', path, body=body)
    
    def get_total_value_by_address(
        self,
        request: TotalValueRequest
    ) -> TotalValueResponse:
        """Get total asset value for an address."""
        chains = request.chains
        if isinstance(chains, list):
            chains = ",".join(map(str, chains))
            
        params = {
            "address": request.address,
            "chains": chains,
            "assetType": request.asset_type,
            "excludeRiskToken": str(request.exclude_risk_token).lower()
        }
        
        response = self.get("/api/v5/wallet/asset/total-value-by-address", params=params)
        return TotalValueResponse.from_api_response(response)

    def get_all_token_balances_by_address(
        self,
        request: TokenBalancesRequest
    ) -> TokenBalancesResponse:
        """Get token balances for an address across chains."""
        chains = request.chains
        if isinstance(chains, list):
            chains = ",".join(map(str, chains))
            
        params = {
            "address": request.address,
            "chains": chains,
        }
        
        if request.filter is not None:
            params["filter"] = request.filter
            
        response = self.get("/api/v5/wallet/asset/all-token-balances-by-address", params=params)
        return TokenBalancesResponse.from_api_response(response)