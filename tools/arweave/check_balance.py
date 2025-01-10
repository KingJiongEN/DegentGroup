import json
from typing import Union, Optional
from dataclasses import dataclass
import requests
from arweave.arweave_lib import Wallet

@dataclass
class WalletBalance:
    address: str
    balance_winston: int
    balance_ar: float
    ar_price_usd: Optional[float] = None
    value_usd: Optional[float] = None

class ArweaveBalance:
    def __init__(self):
        self.ar_node = "https://arweave.net"
        self.price_api = "https://api.coingecko.com/api/v3/simple/price?ids=arweave&vs_currencies=usd"
    
    def _get_ar_price(self) -> Optional[float]:
        """Get current AR price in USD"""
        try:
            response = requests.get(self.price_api, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('arweave', {}).get('usd')
        except Exception as e:
            print(f"Warning: Failed to get AR price: {e}")
        return None

    def _winston_to_ar(self, winston: int) -> float:
        """Convert Winston to AR"""
        return float(winston) / 1000000000000

    def check_by_address(self, address: str) -> WalletBalance:
        """
        Check balance by wallet address
        
        Args:
            address: Arweave wallet address
            
        Returns:
            WalletBalance object
            
        Raises:
            Exception: If balance check fails
        """
        try:
            response = requests.get(
                f"{self.ar_node}/wallet/{address}/balance",
                timeout=5
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to get balance: {response.status_code}")
                
            balance_winston = int(response.text)
            balance_ar = self._winston_to_ar(balance_winston)
            
            ar_price = self._get_ar_price()
            value_usd = balance_ar * ar_price if ar_price else None
            
            return WalletBalance(
                address=address,
                balance_winston=balance_winston,
                balance_ar=balance_ar,
                ar_price_usd=ar_price,
                value_usd=value_usd
            )
            
        except Exception as e:
            raise Exception(f"Failed to check balance: {str(e)}")

    def check_by_jwk(self, jwk_path: str) -> WalletBalance:
        """
        Check balance using JWK file
        
        Args:
            jwk_path: Path to JWK wallet file
            
        Returns:
            WalletBalance object
            
        Raises:
            Exception: If JWK file invalid or balance check fails
        """
        try:
            with open(jwk_path, 'r') as f:
                jwk_data = json.load(f)
                
            wallet = Wallet.from_data(jwk_data)
            return self.check_by_address(wallet.address)
            
        except Exception as e:
            raise Exception(f"Failed to load JWK file or check balance: {str(e)}")

def format_balance(balance: WalletBalance) -> str:
    """Format balance information for display"""
    lines = [
        f"Address: {balance.address}",
        f"Balance: {balance.balance_ar:.6f} AR",
        f"Balance (Winston): {balance.balance_winston}",
    ]
    
    if balance.ar_price_usd:
        lines.extend([
            f"AR Price: ${balance.ar_price_usd:.2f}",
            f"Value: ${balance.value_usd:.2f}"
        ])
        
    return "\n".join(lines)

def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check Arweave wallet balance")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--address", help="Arweave wallet address")
    group.add_argument("--jwk", help="Path to JWK wallet file")
    
    args = parser.parse_args()
    
    try:
        checker = ArweaveBalance()
        
        if args.address:
            balance = checker.check_by_address(args.address)
        else:
            balance = checker.check_by_jwk(args.jwk)
            
        print(format_balance(balance))
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()