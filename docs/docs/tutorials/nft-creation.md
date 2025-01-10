# NFT Creation Tutorial

This tutorial will guide you through implementing NFT creation functionality in your TeleAgent bot.

## Overview

We'll create a system that can:
1. Generate AI artwork using DALL-E
2. Create NFTs from the artwork
3. Handle NFT metadata
4. Implement minting process
5. Enable NFT transfers

## Prerequisites

- Completed [Basic Bot Setup](basic-bot.md)
- OpenAI API key for DALL-E
- Solana wallet setup
- IPFS node access (optional)

## Project Structure

```
nft_bot/
├── artwork/
│   ├── generator.py
│   └── storage.py
├── nft/
│   ├── metadata.py
│   ├── minter.py
│   └── transfer.py
├── config/
│   └── config.py
└── main.py
```

## Step 1: Artwork Generation Setup

```python
# artwork/generator.py
from teleAgent.models.agent_model.artwork_creation import CreativeArtistAgent
from teleAgent.models.agent_model.artwork_creation.dalle_draw import DalleDrawer

class ArtworkGenerator:
    def __init__(self, config: dict):
        self.artist = CreativeArtistAgent(
            character_profile="creative and artistic",
            dalle_config=config["dalle"],
            llm_config=config["llm"]
        )
        self.drawer = DalleDrawer(config["dalle"])
        
    async def generate_artwork(self, prompt: str) -> dict:
        """Generate artwork from prompt"""
        try:
            # Generate enhanced prompt
            enhanced_prompt = await self.artist.enhance_prompt(prompt)
            
            # Generate image
            artwork = await self.drawer.generate_image(enhanced_prompt)
            
            return {
                "image_url": artwork["url"],
                "prompt": enhanced_prompt,
                "metadata": artwork["metadata"]
            }
        except Exception as e:
            logger.error(f"Artwork generation failed: {e}")
            raise
```

## Step 2: NFT Metadata Handling

```python
# nft/metadata.py
from datetime import datetime
import json

class NFTMetadata:
    def __init__(self, artwork_data: dict):
        self.artwork_data = artwork_data
        
    def generate_metadata(self) -> dict:
        """Generate NFT metadata"""
        return {
            "name": f"TeleAgent NFT #{int(time.time())}",
            "description": self.artwork_data["prompt"],
            "image": self.artwork_data["image_url"],
            "attributes": [
                {
                    "trait_type": "Artist",
                    "value": "TeleAgent AI"
                },
                {
                    "trait_type": "Creation Date",
                    "value": datetime.now().isoformat()
                }
            ],
            "properties": {
                "files": [
                    {
                        "uri": self.artwork_data["image_url"],
                        "type": "image/png"
                    }
                ],
                "category": "image",
                "creators": [
                    {
                        "address": "YOUR_CREATOR_ADDRESS",
                        "share": 100
                    }
                ]
            }
        }
```

## Step 3: NFT Minting Implementation

```python
# nft/minter.py
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from spl.token.instructions import create_mint, mint_to

class NFTMinter:
    def __init__(self, config: dict):
        self.client = AsyncClient(config["rpc_url"])
        self.wallet = config["wallet"]
        
    async def mint_nft(self, metadata: dict) -> str:
        """Mint NFT with provided metadata"""
        try:
            # Create mint transaction
            mint_account = await self._create_mint_account()
            
            # Upload metadata to IPFS/Arweave
            metadata_url = await self._upload_metadata(metadata)
            
            # Create mint instruction
            mint_ix = create_mint(
                mint_account.public_key(),
                self.wallet.public_key(),
                0,  # decimals
                self.wallet.public_key()
            )
            
            # Send transaction
            tx = Transaction().add(mint_ix)
            result = await self.client.send_transaction(
                tx,
                self.wallet
            )
            
            return result["result"]
            
        except Exception as e:
            logger.error(f"Minting failed: {e}")
            raise
```

## Step 4: Command Implementation

```python
# main.py
from artwork.generator import ArtworkGenerator
from nft.metadata import NFTMetadata
from nft.minter import NFTMinter

class NFTCommands:
    def __init__(self, client: TelegramClient):
        self.client = client
        self.generator = ArtworkGenerator(config)
        self.minter = NFTMinter(config)
        
    async def setup_handlers(self):
        @self.client.on_command("create_nft")
        async def create_nft(message):
            try:
                # Send processing message
                status_message = await self.client.send_message(
                    chat_id=message.chat.id,
                    text="🎨 Generating your NFT..."
                )
                
                # Generate artwork
                artwork = await self.generator.generate_artwork(
                    message.text
                )
                
                # Update status
                await self.client.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=status_message.message_id,
                    text="🖼️ Artwork generated! Creating NFT..."
                )
                
                # Generate metadata
                metadata = NFTMetadata(artwork).generate_metadata()
                
                # Mint NFT
                mint_result = await self.minter.mint_nft(metadata)
                
                # Send success message
                await self.client.send_photo(
                    chat_id=message.chat.id,
                    photo=artwork["image_url"],
                    caption=f"✨ Your NFT has been created!\n"
                           f"Mint address: {mint_result}"
                )
                
            except Exception as e:
                await self.client.send_message(
                    chat_id=message.chat.id,
                    text=f"❌ Failed to create NFT: {str(e)}"
                )
```

## Step 5: NFT Transfer Implementation

```python
# nft/transfer.py
class NFTTransfer:
    def __init__(self, config: dict):
        self.client = AsyncClient(config["rpc_url"])
        self.wallet = config["wallet"]
        
    async def transfer_nft(
        self,
        mint_address: str,
        recipient: str
    ) -> str:
        """Transfer NFT to recipient"""
        try:
            # Create transfer instruction
            transfer_ix = spl.token.instructions.transfer(
                mint_address,
                self.wallet.public_key(),
                recipient,
                1  # amount (always 1 for NFTs)
            )
            
            # Send transaction
            tx = Transaction().add(transfer_ix)
            result = await self.client.send_transaction(
                tx,
                self.wallet
            )
            
            return result["result"]
            
        except Exception as e:
            logger.error(f"Transfer failed: {e}")
            raise
```

## Step 6: Adding Transfer Commands

```python
@client.on_command("transfer_nft")
async def transfer_nft(message):
    try:
        # Parse command arguments
        args = message.text.split()
        if len(args) != 3:
            raise ValueError(
                "Usage: /transfer_nft <mint_address> <recipient_address>"
            )
            
        mint_address = args[1]
        recipient = args[2]
        
        # Send processing message
        status_message = await client.send_message(
            chat_id=message.chat.id,
            text="🔄 Processing NFT transfer..."
        )
        
        # Execute transfer
        result = await nft_transfer.transfer_nft(
            mint_address,
            recipient
        )
        
        # Send success message
        await client.edit_message_text(
            chat_id=message.chat.id,
            message_id=status_message.message_id,
            text=f"✅ NFT transferred successfully!\n"
                 f"Transaction: {result}"
        )
        
    except Exception as e:
        await client.send_message(
            chat_id=message.chat.id,
            text=f"❌ Transfer failed: {str(e)}"
        )
```

## Best Practices

1. **Error Handling**
   ```python
   try:
       result = await operation()
   except NFTMintError as e:
       logger.error(f"Minting error: {e}")
       # Implement retry logic
   except TransferError as e:
       logger.error(f"Transfer error: {e}")
       # Notify user and suggest solutions
   ```

2. **Rate Limiting**
   ```python
   from teleAgent.utilities.rate_limiter import RateLimiter

   rate_limiter = RateLimiter(
       max_requests=1,  # One NFT creation per minute
       time_window=60
   )

   @rate_limiter.limit
   async def create_nft(message):
       # NFT creation logic
       pass
   ```

3. **Metadata Storage**
   ```python
   async def store_metadata(metadata: dict):
       """Store metadata in IPFS"""
       ipfs_client = IPFSClient()
       cid = await ipfs_client.add_json(metadata)
       return f"ipfs://{cid}"
   ```

## Testing

```python
# test_nft.py
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_nft_creation():
    # Mock dependencies
    artwork_mock = AsyncMock()
    artwork_mock.generate_artwork.return_value = {
        "image_url": "http://example.com/image.png",
        "prompt": "Test prompt"
    }
    
    minter_mock = AsyncMock()
    minter_mock.mint_nft.return_value = "mint_address"
    
    # Test creation
    result = await create_nft(artwork_mock, minter_mock, "test prompt")
    assert result["mint_address"] == "mint_address"
```

## Troubleshooting

1. **Artwork Generation Issues**
   - Check DALL-E API key
   - Verify prompt formatting
   - Monitor rate limits

2. **Minting Problems**
   - Check wallet balance
   - Verify network connection
   - Validate metadata format

3. **Transfer Issues**
   - Verify ownership
   - Check recipient address
   - Confirm gas fees

## Next Steps

1. Implement additional features:
   - NFT collections
   - Batch minting
   - Royalties

2. Add advanced functionality:
   - Secondary market
   - Price discovery
   - Automated trading

3. Explore other tutorials:
   - [Group Chat Integration](group-chat.md)
   - [Bargaining System](bargaining-system.md) 