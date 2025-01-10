from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import asyncio
import traceback

from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price
from solana.rpc.async_api import AsyncClient
from solana.rpc import types as rpc_types
from solana.transaction import Transaction

from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from spl.token.instructions import (
    get_associated_token_address,
    create_associated_token_account,
    TransferParams,
    transfer
)

from teleAgent.core.config import settings
from teleAgent.logger.logger import get_logger

logger = get_logger("plugin_solana:tools:transfer_nft")

@dataclass
class NFTTransferResult:
    success: bool
    tx_hash: Optional[str]
    from_address: str
    to_address: str  
    token_id: str
    price: Optional[float]
    timestamp: datetime
    error: Optional[str]

async def transfer_nft(
    token_id: str,
    to_address: str,
    price: Optional[float] = None,
    memo: Optional[str] = None
) -> NFTTransferResult:
    client = None
    try:
        if not settings.METAPLEX_PRIVATE_KEY:
            raise ValueError("Metaplex private key not configured")

        client = AsyncClient(settings.SOLANA_RPC_URL)
        payer = Keypair.from_base58_string(settings.METAPLEX_PRIVATE_KEY)
        
        # Convert addresses to Pubkeys
        mint_pubkey = Pubkey.from_string(token_id)
        dest_pubkey = Pubkey.from_string(to_address)

        # Get sender's Associated Token Account (ATA)
        sender_ata = get_associated_token_address(
            owner=payer.pubkey(),
            mint=mint_pubkey
        )

        # Get recipient's Associated Token Account (ATA)
        recipient_ata = get_associated_token_address(
            owner=dest_pubkey,
            mint=mint_pubkey
        )

        # Check if recipient's ATA exists, if not create it
        ata_info = await client.get_account_info(recipient_ata)
        
        tx = Transaction()
        tx.fee_payer = payer.pubkey()
        set_compute_unit_limit_ix = set_compute_unit_limit(300000)
        tx.add(set_compute_unit_limit_ix)

        set_compute_unit_price_ix = set_compute_unit_price(20000)
        tx.add(set_compute_unit_price_ix)

        if not ata_info.value:
            create_ata_ix = create_associated_token_account(
                payer=payer.pubkey(),
                owner=dest_pubkey,
                mint=mint_pubkey
            )
            tx.add(create_ata_ix)

        # Create transfer instruction using TransferParams
        transfer_params = TransferParams(
            amount=1,  # Amount is always 1 for NFTs
            dest=recipient_ata,
            owner=payer.pubkey(),
            program_id=TOKEN_PROGRAM_ID,
            source=sender_ata,
            signers=None  # Optional signers if using a delegate
        )
        
        transfer_ix = transfer(transfer_params)
        tx.add(transfer_ix)
        
        # Send and confirm transaction with retry logic
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                recent_blockhash = await client.get_latest_blockhash()
                logger.info(f"recent blockhash: {recent_blockhash}")
                tx.recent_blockhash = recent_blockhash.value.blockhash

                logger.info("sign")
                tx.sign(payer)
            
                sig = await client.send_transaction(
                    tx.serialize(),
                    opts=rpc_types.TxOpts(
                        skip_preflight=False,
                        preflight_commitment="confirmed"
                    )
                )

                confirmation = await client.confirm_transaction(
                    sig.value,
                    commitment="confirmed",
                    sleep_seconds=1,
                    last_valid_block_height=None,
                )

                if not confirmation.value or confirmation.value[0] is None:
                    logger.error("Transaction status not found")
                    raise Exception("Transaction status not found")

                if confirmation.value[0].err:
                    logger.error(f"Transaction failed: {confirmation.value[0].err}")
                    raise Exception(f"Transaction failed: {confirmation.value[0].err}")

                break
                
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    raise Exception(f"Transaction failed after {max_retries} retries: {str(e)}")
                await asyncio.sleep(2 ** retry_count)

        return NFTTransferResult(
            success=True,
            tx_hash=str(sig.value),
            from_address=str(payer.pubkey()),
            to_address=to_address,
            token_id=token_id,
            price=price,
            timestamp=datetime.now(),
            error=None
        )

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error transferring NFT:\n{error_trace}")
        return NFTTransferResult(
            success=False,
            tx_hash=None,
            from_address=str(payer.pubkey()) if 'payer' in locals() else "",
            to_address=to_address,
            token_id=token_id,
            price=price,
            timestamp=datetime.now(),
            error=f"{str(e)}\nStack trace:\n{error_trace}"
        )

    finally:
        if client:
            await client.close()