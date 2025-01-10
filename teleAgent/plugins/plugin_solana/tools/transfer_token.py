from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union, Dict
import asyncio
import traceback
import struct

from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price
from solders.system_program import TransferParams, transfer
from solana.rpc.async_api import AsyncClient
from solana.rpc import types as rpc_types
from solana.transaction import Transaction

from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from spl.token.instructions import (
    get_associated_token_address,
    create_associated_token_account,
    TransferParams as TokenTransferParams,
    transfer as token_transfer
)

from teleAgent.core.config import settings
from teleAgent.logger.logger import get_logger

logger = get_logger("plugin_solana:tools:transfer_token")

MINT_LEN: int = 82
DECIMALS_LAYOUT = struct.Struct("B")
DECIMALS_OFFSET: int = 44

@dataclass
class TokenTransferResult:
    success: bool
    tx_hash: Optional[str]
    from_address: str  
    to_address: str
    token_mint: Optional[str]
    amount: float
    fee: float
    timestamp: datetime
    error: Optional[str]

async def get_token_decimals(client: AsyncClient, mint_address: Pubkey) -> int:
    """Get token decimals from mint account"""
    try:
        account_info = await client.get_account_info(mint_address)
        if not account_info.value:
            raise ValueError(f"Mint account {mint_address} not found")
            
        # Validate mint account data length
        data = account_info.value.data
        if len(data) < MINT_LEN:
            raise ValueError(f"Invalid mint account data length: {len(data)}")
            
        # Extract decimals value
        (decimals,) = DECIMALS_LAYOUT.unpack_from(data, DECIMALS_OFFSET)
        return decimals
        
    except Exception as e:
        raise ValueError(f"Failed to get token decimals: {str(e)}")

async def transfer_token(
    to_address: str,
    amount: float,
    token_mint: Optional[str] = None,
    memo: Optional[str] = None,
    skip_preflight: bool = False
) -> TokenTransferResult:
    client = None
    try:
        if not settings.METAPLEX_PRIVATE_KEY:
            raise ValueError("Wallet private key not configured")

        client = AsyncClient(settings.SOLANA_RPC_URL)
        payer = Keypair.from_base58_string(settings.METAPLEX_PRIVATE_KEY)
        dest_pubkey = Pubkey.from_string(to_address)

        # Get decimals based on token type
        decimals = 9  # Default for SOL
        if token_mint:
            mint_pubkey = Pubkey.from_string(token_mint)
            decimals = await get_token_decimals(client, mint_pubkey)

        tx = Transaction()
        tx.fee_payer = payer.pubkey()
        set_compute_unit_limit_ix = set_compute_unit_limit(300000)
        tx.add(set_compute_unit_limit_ix)

        set_compute_unit_price_ix = set_compute_unit_price(20000)
        tx.add(set_compute_unit_price_ix)

        if token_mint is None:
            # SOL transfer using solders
            tx_instruction = transfer(
                TransferParams(
                    from_pubkey=payer.pubkey(),
                    to_pubkey=dest_pubkey,
                    lamports=int(amount * (10 ** decimals))
                )
            )
            tx.add(tx_instruction)
        else:
            mint_pubkey = Pubkey.from_string(token_mint)
            sender_ata = get_associated_token_address(payer.pubkey(), mint_pubkey)
            recipient_ata = get_associated_token_address(dest_pubkey, mint_pubkey)

            ata_info = await client.get_account_info(recipient_ata)
            if not ata_info.value:
                create_ata_ix = create_associated_token_account(
                    payer=payer.pubkey(),
                    owner=dest_pubkey,
                    mint=mint_pubkey
                )
                tx.add(create_ata_ix)

            transfer_ix = token_transfer(
                TokenTransferParams(
                    amount=int(amount * (10 ** decimals)),
                    dest=recipient_ata,
                    owner=payer.pubkey(),
                    program_id=TOKEN_PROGRAM_ID,
                    source=sender_ata
                )
            )
            tx.add(transfer_ix)

        max_retries = 3
        retry_count = 0
        last_error = None

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
                        skip_preflight=skip_preflight,
                        preflight_commitment="confirmed"
                    )
                )

                confirmation = await client.confirm_transaction(
                    sig.value,
                    commitment="confirmed",
                    sleep_seconds=1,
                    last_valid_block_height=None
                )

                if not confirmation.value or confirmation.value[0] is None:
                    raise Exception("Transaction status not found")

                if confirmation.value[0].err:
                    logger.error(f"Transaction failed: {confirmation.value[0].err}")
                    raise Exception(f"Transaction failed: {confirmation.value[0].err}")

                return TokenTransferResult(
                    success=True,
                    tx_hash=str(sig.value),
                    from_address=str(payer.pubkey()),
                    to_address=to_address,
                    token_mint=token_mint,
                    amount=amount,
                    fee=0.000005,
                    timestamp=datetime.now(),
                    error=None
                )

            except Exception as e:
                last_error = e
                retry_count += 1
                if retry_count < max_retries:
                    await asyncio.sleep(2 ** retry_count)
                    continue
                break

        raise Exception(f"Transaction failed after {max_retries} retries: {str(last_error)}")

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error transferring tokens:\n{error_trace}")
        return TokenTransferResult(
            success=False,
            tx_hash=None,
            from_address=str(payer.pubkey()) if 'payer' in locals() else "",
            to_address=to_address,
            token_mint=token_mint,
            amount=amount,
            fee=0,
            timestamp=datetime.now(),
            error=f"{str(e)}\nTrace:\n{error_trace}"
        )

    finally:
        if client:
            await client.close()