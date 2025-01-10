import json
import hashlib
import base64
from typing import Tuple
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from base64 import b64encode
from arweave.arweave_lib import Wallet
import requests

def generate_arweave_wallet(output_path: str = "arweave-key.json") -> Tuple[dict, str]:
    """
    Generate new Arweave JWK wallet and return address
    
    Args:
        output_path: Path to save the JWK file
        
    Returns:
        Tuple of (JWK wallet data as dict, wallet address)
    """
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )
    
    # Get public key
    public_key = private_key.public_key()
    
    # Extract components
    private_numbers = private_key.private_numbers()
    public_numbers = public_key.public_numbers()
    
    # Create JWK format
    jwk = {
        "kty": "RSA",
        "e": b64encode(public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, byteorder='big')).decode('utf-8'),
        "n": b64encode(public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, byteorder='big')).decode('utf-8'),
        "d": b64encode(private_numbers.d.to_bytes((private_numbers.d.bit_length() + 7) // 8, byteorder='big')).decode('utf-8'),
        "p": b64encode(private_numbers.p.to_bytes((private_numbers.p.bit_length() + 7) // 8, byteorder='big')).decode('utf-8'),
        "q": b64encode(private_numbers.q.to_bytes((private_numbers.q.bit_length() + 7) // 8, byteorder='big')).decode('utf-8'),
        "dp": b64encode(private_numbers.dmp1.to_bytes((private_numbers.dmp1.bit_length() + 7) // 8, byteorder='big')).decode('utf-8'),
        "dq": b64encode(private_numbers.dmq1.to_bytes((private_numbers.dmq1.bit_length() + 7) // 8, byteorder='big')).decode('utf-8'),
        "qi": b64encode(private_numbers.iqmp.to_bytes((private_numbers.iqmp.bit_length() + 7) // 8, byteorder='big')).decode('utf-8')
    }
    
    # Save to file
    with open(output_path, 'w') as f:
        json.dump(jwk, f, indent=2)
    
    # Get wallet address
    wallet = Wallet.from_data(jwk)
    address = wallet.address
        
    return jwk, address

def get_wallet_info(jwk_data: dict) -> dict:
    """
    Get wallet address and balance
    
    Args:
        jwk_data: JWK wallet data
        
    Returns:
        Dict with wallet info
    """
    wallet = Wallet.from_data(jwk_data)
    
    # Get balance from Arweave network
    try:
        balance = wallet.balance
        balance_ar = float(balance) / 1000000000000  # Convert Winston to AR
    except:
        balance_ar = 0
    
    return {
        "address": wallet.address,
        "balance": balance_ar,
        "balance_winston": str(balance)
    }

 

if __name__ == "__main__":
    # Generate new wallet
    jwk, address = generate_arweave_wallet()
    
    # Get wallet info
    wallet_info = get_wallet_info(jwk)
    
    print("\nWallet generated successfully!")
    print(f"Address: {wallet_info['address']}")
    print(f"Balance: {wallet_info['balance']} AR")
    print("\nTo get AR tokens:")
    print("1. Visit https://faucet.arweave.net")
    print("2. Use exchange like Binance or Gate.io")
    print(f"3. Send AR to address: {wallet_info['address']}")