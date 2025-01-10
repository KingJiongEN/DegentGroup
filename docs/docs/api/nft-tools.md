# NFT Tools API Reference

Comprehensive documentation for the TeleAgent NFT Tools system, which handles NFT creation, management, and transactions.

## NFTCreator

The main class for NFT creation and minting operations.

### Constructor

```python
def __init__(
    self,
    config: dict,
    artwork_dao: ArtworkDAO = None,
    nft_dao: NFTDAO = None
):
    """
    Initialize NFTCreator.
    
    Args:
        config (dict): Configuration containing:
            - wallet_address (str): Creator's wallet address
            - network (str): Blockchain network (e.g., "mainnet", "devnet")
            - api_endpoint (str): RPC endpoint URL
        artwork_dao (ArtworkDAO, optional): Data access object for artwork
        nft_dao (NFTDAO, optional): Data access object for NFTs
            
    Raises:
        ValueError: If required configuration is missing
        ConnectionError: If network connection fails
    """
```

### Core Methods

#### NFT Creation

```python
async def create_nft(
    self,
    artwork: dict,
    metadata: dict,
    options: dict = None
) -> dict:
    """
    Create a new NFT from artwork.
    
    Args:
        artwork: Artwork information containing:
            - image_url (str): URL of the artwork
            - title (str): Artwork title
            - description (str): Artwork description
        metadata: NFT metadata containing:
            - attributes (list): NFT attributes
            - properties (dict): Additional properties
        options: Optional creation parameters:
            - royalty_percentage (float): Creator royalty
            - is_mutable (bool): Whether metadata can be updated
            
    Returns:
        dict: Created NFT information containing:
            - mint_address (str): NFT mint address
            - metadata_url (str): Metadata URL
            - transaction_id (str): Creation transaction ID
            
    Raises:
        NFTCreationError: If NFT creation fails
    """

async def mint_nft(
    self,
    mint_address: str,
    recipient_address: str = None
) -> dict:
    """
    Mint an NFT to a recipient.
    
    Args:
        mint_address: NFT mint address
        recipient_address: Optional recipient wallet address
            (defaults to creator's address)
            
    Returns:
        dict: Minting result containing:
            - transaction_id (str): Minting transaction ID
            - recipient (str): Recipient wallet address
            
    Raises:
        MintingError: If minting operation fails
    """
```

#### Metadata Management

```python
class MetadataManager:
    def __init__(self, storage_config: dict):
        """
        Initialize metadata manager.
        
        Args:
            storage_config: Storage configuration containing:
                - provider (str): Storage provider (e.g., "arweave", "ipfs")
                - endpoint (str): Storage endpoint URL
        """
        
    async def upload_metadata(
        self,
        metadata: dict,
        is_mutable: bool = False
    ) -> str:
        """
        Upload NFT metadata to storage.
        
        Args:
            metadata: NFT metadata
            is_mutable: Whether metadata can be updated
            
        Returns:
            str: Metadata URL
            
        Raises:
            StorageError: If upload fails
        """
        
    async def update_metadata(
        self,
        metadata_url: str,
        updates: dict
    ) -> str:
        """
        Update existing NFT metadata.
        
        Args:
            metadata_url: Current metadata URL
            updates: Metadata updates to apply
            
        Returns:
            str: New metadata URL
            
        Raises:
            StorageError: If update fails
            ImmutableError: If metadata is immutable
        """
```

### Transaction Management

```python
class TransactionManager:
    def __init__(self, network_config: dict):
        self.client = AsyncClient(network_config["endpoint"])
        
    async def send_transaction(
        self,
        transaction: Transaction,
        signers: List[Keypair]
    ) -> str:
        """
        Send and confirm transaction.
        
        Args:
            transaction: Transaction to send
            signers: Required transaction signers
            
        Returns:
            str: Transaction signature
            
        Raises:
            TransactionError: If transaction fails
        """
        
    async def verify_transaction(
        self,
        signature: str
    ) -> dict:
        """
        Verify transaction status.
        
        Args:
            signature: Transaction signature
            
        Returns:
            dict: Transaction status and details
        """
```

### NFT Transfer

```python
async def transfer_nft(
    self,
    mint_address: str,
    recipient_address: str,
    options: dict = None
) -> dict:
    """
    Transfer NFT to new owner.
    
    Args:
        mint_address: NFT mint address
        recipient_address: Recipient wallet address
        options: Optional transfer parameters:
            - skip_preflight (bool): Skip preflight check
            - max_retries (int): Maximum retry attempts
            
    Returns:
        dict: Transfer result containing:
            - transaction_id (str): Transfer transaction ID
            - old_owner (str): Previous owner address
            - new_owner (str): New owner address
            
    Raises:
        TransferError: If transfer fails
    """
```

### Usage Examples

#### Basic NFT Creation

```python
from teleAgent.nft.creator import NFTCreator

# Initialize creator
creator = NFTCreator({
    "wallet_address": "YOUR_WALLET_ADDRESS",
    "network": "devnet",
    "api_endpoint": "https://api.devnet.solana.com"
})

# Create NFT
nft = await creator.create_nft(
    artwork={
        "image_url": "https://example.com/art.png",
        "title": "My First NFT",
        "description": "A beautiful artwork"
    },
    metadata={
        "attributes": [
            {"trait_type": "Background", "value": "Blue"},
            {"trait_type": "Style", "value": "Abstract"}
        ],
        "properties": {
            "files": [{"uri": "https://example.com/art.png", "type": "image/png"}],
            "category": "image"
        }
    }
)
```

#### NFT Transfer

```python
# Transfer NFT
transfer_result = await creator.transfer_nft(
    mint_address="NFT_MINT_ADDRESS",
    recipient_address="RECIPIENT_ADDRESS",
    options={
        "skip_preflight": False,
        "max_retries": 3
    }
)

# Verify transfer
status = await creator.transaction_manager.verify_transaction(
    transfer_result["transaction_id"]
)
```

### Error Handling

```python
class NFTError(Exception):
    """Base exception for NFT-related errors"""
    pass

class NFTCreationError(NFTError):
    """Exception for NFT creation failures"""
    pass

class MintingError(NFTError):
    """Exception for minting failures"""
    pass

class TransferError(NFTError):
    """Exception for transfer failures"""
    pass

try:
    nft = await creator.create_nft(artwork, metadata)
except NFTCreationError as e:
    logger.error(f"Creation failed: {e}")
    # Handle creation failure
except MintingError as e:
    logger.error(f"Minting failed: {e}")
    # Handle minting failure
except NFTError as e:
    logger.error(f"NFT operation failed: {e}")
    # Handle other errors
```

### Best Practices

1. **Transaction Safety**
   ```python
   async def safe_transfer(mint_address: str, recipient: str) -> dict:
       """Implement safe transfer with verification"""
       # Verify ownership
       if not await verify_ownership(mint_address):
           raise OwnershipError("Not the owner")
           
       # Check recipient account
       if not await verify_recipient(recipient):
           raise RecipientError("Invalid recipient")
           
       # Execute transfer
       result = await transfer_nft(mint_address, recipient)
       
       # Verify transfer
       status = await verify_transaction(result["transaction_id"])
       if not status["success"]:
           raise TransferError("Transfer failed")
           
       return result
   ```

2. **Metadata Validation**
   ```python
   def validate_metadata(metadata: dict) -> bool:
       """Validate NFT metadata structure"""
       required_fields = ["name", "description", "image"]
       return all(field in metadata for field in required_fields)
   ```

3. **Rate Limiting**
   ```python
   from teleAgent.utilities.rate_limiter import RateLimiter

   rate_limiter = RateLimiter(
       max_requests=10,  # Maximum requests per window
       time_window=60    # Window size in seconds
   )

   @rate_limiter.limit
   async def create_nft(artwork: dict, metadata: dict):
       # NFT creation logic
       pass
   ``` 