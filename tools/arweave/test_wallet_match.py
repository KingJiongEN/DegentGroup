import json
import base64
import logging
from pathlib import Path
from typing import Dict, Optional
from arweave.arweave_lib import Wallet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_jwk_wallet(jwk_path: str, expected_address: Optional[str] = None) -> Dict:
    """
    Verify JWK file and optionally check if it matches an expected address
    
    Args:
        jwk_path: Path to JWK file
        expected_address: Expected wallet address to verify against (optional)
        
    Returns:
        Dict containing verification results
    """
    try:
        # Load and validate JWK file
        with open(jwk_path, 'r') as f:
            jwk_data = json.load(f)
            
        # Verify required JWK fields
        required_fields = ['kty', 'n', 'e']
        missing_fields = [field for field in required_fields if field not in jwk_data]
        if missing_fields:
            raise ValueError(f"Missing required JWK fields: {missing_fields}")
            
        # Create wallet from JWK
        wallet = Wallet.from_data(jwk_data)
        actual_address = wallet.address
        
        result = {
            'jwk_path': jwk_path,
            'is_valid_jwk': True,
            'actual_address': actual_address,
            'matches_expected': None
        }
        
        # Check against expected address if provided
        if expected_address:
            result['expected_address'] = expected_address
            result['matches_expected'] = (actual_address == expected_address)
        
        return result
        
    except Exception as e:
        logger.error(f"Error verifying {jwk_path}: {str(e)}")
        return {
            'jwk_path': jwk_path,
            'is_valid_jwk': False,
            'error': str(e)
        }

def verify_all_jwk_files(expected_addresses: Dict[str, str] = None):
    """
    Verify all JWK files in a directory
    
    Args:
        directory: Directory containing JWK files
        expected_addresses: Dict mapping filenames to expected addresses
    """
    results = []
    for jwk_path, expected_address in expected_addresses.items():
        result = verify_jwk_wallet(jwk_path, expected_address)
        results.append(result)
        
        # Log results
        if result['is_valid_jwk']:
            logger.info(f"\nVerified {jwk_path}:")
            logger.info(f"  Address: {result['actual_address']}")
            if 'matches_expected' in result and 'expected_address' in result:
                match_status = "✓ Matches" if result['matches_expected'] else "✗ Does NOT match"
                logger.info(f"  Expected: {result['expected_address']}")
                logger.info(f"  Status: {match_status}")
        else:
            logger.error(f"\nFailed to verify {jwk_path}:")
            logger.error(f"  Error: {result['error']}")

    return results

if __name__ == "__main__":
    # Example expected addresses (replace with actual addresses)
    expected_addresses = {
        "agents/bot-1/bot-1-jwk.json": "24b77A3TBwmoWkbJk1bJ3cmXFHEyS6fXGr1j2CKPQsbe",
        "agents/bot-2/bot-2-jwk.json": "6tfRLfdAVU3xRfsWmFuELgV5yX9tyCJ1yhrQaR84X6oF",
        "agents/bot-3/bot-3-jwk.json": "8xwW69ZU86j7mwFPZWwVEKzBsKhuSGKYcyih1H2odaKR"
    }
    
    # Test specific JWK file
    # single_result = verify_jwk_wallet("agents/bot-1/jwk/bot-1-jwk.json")
    # logger.info("\nSingle JWK verification result:")
    # logger.info(json.dumps(single_result, indent=2))
    
    # Test all JWK files in agents directory
    logger.info("\nVerifying all JWK files:")
    all_results = verify_all_jwk_files(expected_addresses)
