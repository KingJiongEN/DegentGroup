import json
from typing import Union, BinaryIO
import logging
from arweave.arweave_lib import Wallet, Transaction
from arweave.transaction_uploader import get_uploader
from teleAgent.core.config import settings
from teleAgent.core.config import settings

from teleAgent.plugins.plugin_solana.utils.arweave.transaction import EnhancedTransaction

logger = logging.getLogger(__name__)

async def upload_to_arweave(data: Union[bytes, dict, BinaryIO]) -> str:
    """
    Upload data to Arweave permanent storage
    
    Args:
        data: Binary data, file handler or dict to upload
        
    Returns:
        Arweave URL for uploaded content
        
    Raises:
        Exception: If upload fails
    """
    try:
        wallet = Wallet(settings.ARWEAVE_JWK_FILE)

        if isinstance(data, dict):
            # Handle JSON metadata
            upload_data = json.dumps(data).encode()
            tx = EnhancedTransaction(wallet, data=upload_data)
            tx.add_tag('Content-Type', 'application/json')
            
            # Remove await as these are not async methods
            tx.sign()
            tx.send()
            
            return f"https://arweave.net/{tx.id}"

        elif isinstance(data, BinaryIO):
            # Handle file upload with chunks
            tx = EnhancedTransaction(wallet, file_handler=data)
            tx.add_tag('Content-Type', 'image/png')
            
            tx.sign()
            
            # Uploader might still need to be async
            uploader = get_uploader(tx, data)
            while not uploader.is_complete:
                uploader.upload_chunk()  # Remove await if not async
                logger.info(f"Upload progress: {uploader.pct_complete}%")
                
            return f"https://arweave.net/{tx.id}"

        else:
            # Handle raw bytes
            tx = EnhancedTransaction(wallet, data=data)
            tx.add_tag('Content-Type', 'image/png')
            
            tx.sign()
            tx.send()
            
            return f"https://arweave.net/{tx.id}"

    except Exception as e:
        logger.error(f"Arweave upload failed: {str(e)}")
        raise Exception(f"Failed to upload to Arweave: {str(e)}")