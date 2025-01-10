import asyncio
import requests
import traceback
from typing import List, ClassVar, Union, Optional

from pydantic import BaseModel
import borsh_construct as borsh

from solana.rpc import types as rpc_types
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction

from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.instruction import Instruction, AccountMeta
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price

from spl.token.instructions import (
    create_associated_token_account,
    get_associated_token_address,
)

from teleAgent.core.config import settings
from teleAgent.logger.logger import get_logger

# Assume META_PROGRAM_ID is defined elsewhere in your project
META_PROGRAM_ID = Pubkey.from_string("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")

logger = get_logger("plugin_solana:tools:buy_nft")

class NFTAttribute(BaseModel):
    trait_type: str
    value: Union[str, int]

class NFTProperties(BaseModel):
    files: List[dict]
    category: Optional[str] = None
    creators: Optional[List[dict]] = None

class NFTCollection(BaseModel):
    slug: str
    name: str
    description: str
    image: str
    royalty: float
    onChain: bool
    
class NFTTokenInfo(BaseModel):
    mintAddress: str
    owner: str
    supply: int
    collection: str
    collectionName: str
    name: str
    updateAuthority: str
    primarySaleHappened: bool
    sellerFeeBasisPoints: int
    image: str
    externalUrl: Optional[str] = None
    attributes: List[NFTAttribute]
    properties: NFTProperties

class SolPriceInfo(BaseModel):
    rawAmount: str
    address: str
    decimals: int

class PriceInfo(BaseModel):
    solPrice: SolPriceInfo

class NFTListing(BaseModel):
    pdaAddress: str
    auctionHouse: str
    tokenAddress: str
    tokenMint: str
    seller: str
    sellerReferral: str
    tokenSize: int
    price: float
    priceInfo: PriceInfo
    expiry: int
    token: NFTTokenInfo
    listingSource: str

def derive_metadata_key(mint_pubkey: Pubkey) -> Pubkey:
    """
    Custom implementation of derive_metadata_key based on the provided logic.

    Args:
        mint_pubkey: The public key of the mint account.

    Returns:
        The derived metadata account address as a Pubkey.
    """

    metadata_seeds = [
        b"metadata",
        bytes(META_PROGRAM_ID),
        bytes(mint_pubkey),
    ]

    metadata_address, _ = Pubkey.find_program_address(
        seeds=metadata_seeds,
        program_id=META_PROGRAM_ID
    )
    return metadata_address


def encode_bytes_init(data: Union[bytes, str, int]) -> bytes:
    """
    Encodes data into a suitable format for PDA seed.
    """
    if isinstance(data, str):
        return data.encode("utf-8")
    elif isinstance(data, int):
        return data.to_bytes((data.bit_length() + 7) // 8, 'little')
    elif isinstance(data, bytes):
      return data
    else:
      raise ValueError(f"Unsupported data type for encoding: {type(data)}")
    
class BuyInstruction:
    layout: ClassVar = borsh.CStruct(
        "buyer_price" / borsh.U64,
        "token_size" / borsh.U64,
        "buyer_state_expiry" / borsh.I64,
        "buyer_creator_royalty_bp" / borsh.U16,
        "extra_args" / borsh.Vec(borsh.U8)
    )

class DepositInstruction:
    layout: ClassVar = borsh.CStruct(
        "escrow_payment_bump" / borsh.U8,
        "amount" / borsh.U64
    )

class ExecuteSaleInstruction:
    layout: ClassVar = borsh.CStruct(
        "escrow_payment_bump" / borsh.U8,
        "program_as_signer_bump" / borsh.U8,
        "buyer_price" / borsh.U64,
        "token_size" / borsh.U64,
        "buyer_state_expiry" / borsh.I64,
        "seller_state_expiry" / borsh.I64,
        "maker_fee_bp" / borsh.I16,
        "taker_fee_bp" / borsh.U16,
    )

class CoreBuyInstruction:
    layout: ClassVar = borsh.CStruct(
        "price" / borsh.U64,
        "maker_fee_bp" / borsh.I16,
        "taker_fee_bp" / borsh.U16,
        "compression_proof" / borsh.Option(borsh.Vec(borsh.U8))
    )

class NFTBuyingService:
    def __init__(self):
        self.client = AsyncClient(settings.SOLANA_RPC_URL)
        self.me_v2_program_id = Pubkey.from_string("M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K")
        self.me_v2_authority = Pubkey.from_string("autMW8SgBkVYeBgqYiTuJZnkvDZMVU2MHJh9Jh7CSQ2")
        self.me_v2_notary = Pubkey.from_string("NTYeYJ1wr4bpM5xo6zx5En44SvJFAd35zTxxNoERYqd")
        self.token_program = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
        self.system_program = Pubkey.from_string("11111111111111111111111111111111")
        self.ata_program = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
        self.rent_program = Pubkey.from_string("SysvarRent111111111111111111111111111111111")
        self.mpl_core_program = Pubkey.from_string("CoREENxT6tW1HoK8ypY1SxRMZTcVPm7R94rH4PZNhX7d")
        self.me_api_base = "https://api-mainnet.magiceden.dev/v2"
        logger.info("NFTBuyingService initialized with Magic Eden V2 program")

    async def get_listing_info(self, token_mint: str) -> NFTListing:
        logger.info(f"Fetching listing info for NFT: {token_mint}")
        url = f"{self.me_api_base}/tokens/{token_mint}/listings?listingAggMode=true"
        
        try:
            response = requests.get(url, headers={"accept": "application/json"})

            if response.status_code != 200:
                error_msg = f"Failed to fetch listing: HTTP {response.status_code}"
                logger.error(error_msg)
                raise ConnectionError(error_msg)
                
            listings = response.json()
            if not listings:
                error_msg = f"No active listings found for NFT: {token_mint}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            logger.error(f"get_listing_info body: {listings}")
            listing = NFTListing.parse_obj(listings[0])
            logger.info(f"Found listing for {listing.token.name} at {listing.price} SOL")
            return listing

        except Exception as e:
            logger.error(f"Error fetching listing info: {str(e)}")
            raise

    async def send_and_confirm_transaction(
        self,
        tx: Transaction,
        wallet: Keypair,
        max_retries: int = 3
    ) -> str:
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                logger.info(f"Sending transaction (attempt {retry_count + 1}/{max_retries})")
                
                recent_blockhash = await self.client.get_latest_blockhash()
                logger.info(f"recent blockhash: {recent_blockhash}")
                tx.recent_blockhash = recent_blockhash.value.blockhash

                logger.info("sign")
                tx.sign(wallet)

                sig = await self.client.send_transaction(
                    tx.serialize(),
                    opts=rpc_types.TxOpts(
                        skip_preflight=False,
                        preflight_commitment="confirmed"
                    )
                )

                confirmation = await self.client.confirm_transaction(
                    sig.value,
                    commitment="confirmed",
                    sleep_seconds=1,
                    last_valid_block_height=None,
                )

                logger.info(f"Transaction status: {confirmation.value}")

                if confirmation.value[0].err:
                    logger.error(f"Transaction failed: {confirmation.value[0].err}")
                    raise Exception(f"Transaction failed: {confirmation.value[0].err}")

                logger.info("Transaction confirmed successfully!")
                return sig.value

            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    error_msg = f"Transaction failed after {max_retries} retries: {str(e)}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                
                wait_time = 2 ** retry_count
                logger.info(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)

    async def is_mpl_core_nft(self, mint: str) -> bool:
        """Check MPL Core NFT"""
        try:
            metadata = await self.client.get_account_info(
                Pubkey.from_string(mint)
            )
            logger.info(f"is_mpl_core_nft metadata: {metadata}")
            return metadata.value.owner == self.mpl_core_program
        except:
            return False
    
    def _create_deposit_instruction(self, wallet: Keypair, listing: NFTListing, price_lamports:int) -> Instruction:
        """
        Creates the deposit instruction for the Magic Eden V2 program
        """
        logger.info("Building deposit instruction")

        auction_house_key = Pubkey.from_string(listing.auctionHouse)
        seller_referral_key = Pubkey.from_string(listing.sellerReferral)  # Assuming sellerReferral is the notary

        escrow_payment_account, escrow_payment_bump = Pubkey.find_program_address(
                seeds=[
                    b"m2",
                    bytes(auction_house_key),
                    bytes(wallet.pubkey()),
                ],
                program_id=self.me_v2_program_id,
            )
        logger.info(f"Calculated Escrow Payment Account: {escrow_payment_account} with bump {escrow_payment_bump}")

        accounts = [
            AccountMeta(pubkey=wallet.pubkey(), is_signer=True, is_writable=True),
            AccountMeta(pubkey=seller_referral_key, is_signer=False, is_writable=False),
            AccountMeta(pubkey=escrow_payment_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=self.me_v2_authority, is_signer=False, is_writable=False), # Authority
            AccountMeta(pubkey=auction_house_key, is_signer=False, is_writable=False),
            AccountMeta(pubkey=self.system_program, is_signer=False, is_writable=False),
        ]

        logger.info("Accounts details:")
        for i, account in enumerate(accounts):
            logger.info(f"Account {i + 1}: pubkey={account.pubkey}, is_signer={account.is_signer}, is_writable={account.is_writable}")


        identifier = b'\xf2#\xc6\x89R\xe1\xf2\xb6'  # Identifier for deposit instruction
        instruction_data = DepositInstruction.layout.build({
            "escrow_payment_bump": escrow_payment_bump,
            "amount": price_lamports + 2000000
            })
        
        data = identifier + instruction_data
        logger.info(f"Instruction data (hex): {data.hex()}")

        instruction = Instruction(
            program_id=self.me_v2_program_id,
            data=data,
            accounts=accounts,
        )

        return instruction

    def _create_buy_instruction(
        self,
        wallet: Keypair,
        listing: NFTListing,
        price_lamports: int,
        token_program: Pubkey,
    ) -> Instruction:
        """
        Creates the buy_v2 instruction for the Magic Eden V2 program.
        """
        logger.info("Building buy instruction")

        token_mint_key = Pubkey.from_string(listing.tokenMint)
        metadata_account = derive_metadata_key(token_mint_key)
        auction_house_key = Pubkey.from_string(listing.auctionHouse)
        notary_key = Pubkey.from_string(listing.sellerReferral)  # Assuming sellerReferral is the notary
        buyer_referral_key = self.me_v2_authority

        escrow_payment_account, _ = Pubkey.find_program_address(
            seeds=[
                b"m2",
                bytes(auction_house_key),
                bytes(wallet.pubkey()),
            ],
            program_id=self.me_v2_program_id,
        )
        logger.info(f"Calculated Escrow Payment Account: {escrow_payment_account}")

        buyer_trade_state, _ = Pubkey.find_program_address(
            seeds=[
                b"m2",
                bytes(wallet.pubkey()),
                bytes(auction_house_key),
                bytes(token_mint_key),
            ],
            program_id=self.me_v2_program_id,
        )
        logger.info(f"Calculated Buyer Trade State: {buyer_trade_state}")

        accounts = [
            AccountMeta(pubkey=wallet.pubkey(), is_signer=True, is_writable=True),
            AccountMeta(pubkey=notary_key, is_signer=False, is_writable=False),
            AccountMeta(pubkey=token_mint_key, is_signer=False, is_writable=False),
            AccountMeta(pubkey=metadata_account, is_signer=False, is_writable=False),
            AccountMeta(pubkey=escrow_payment_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=self.me_v2_authority, is_signer=False, is_writable=False),
            AccountMeta(pubkey=auction_house_key, is_signer=False, is_writable=False), # auctionHouseFeeAccount
            AccountMeta(pubkey=buyer_trade_state, is_signer=False, is_writable=True),
            AccountMeta(pubkey=buyer_referral_key, is_signer=False, is_writable=False),
            AccountMeta(pubkey=token_program, is_signer=False, is_writable=False),
            AccountMeta(pubkey=self.system_program, is_signer=False, is_writable=False),
        ]

        logger.info("Accounts details:")
        for i, account in enumerate(accounts):
            logger.info(f"Account {i + 1}: pubkey={account.pubkey}, is_signer={account.is_signer}, is_writable={account.is_writable}")

        identifier = b'\xb8\x17\xeeag\xc5\xd3=' # this is the identifier for buy_v2 instruction
        instruction_data = BuyInstruction.layout.build({
            "buyer_price": price_lamports,
            "token_size": 1,
            "buyer_state_expiry": 0,
            "buyer_creator_royalty_bp": 0,
            "extra_args": []
        })
        data = identifier + instruction_data
        logger.info(f"Instruction data (hex): {data.hex()}")

        instruction = Instruction(
            program_id=self.me_v2_program_id,
            data=data,
            accounts=accounts,
        )
        
        return instruction

    def _create_execute_sale_instruction(self, wallet: Keypair, listing: NFTListing, price_lamports: int) -> Instruction:
        """
        Creates the execute_sale_v2 instruction for the Magic Eden V2 program
        """
        logger.info("Building execute_sale_v2 instruction")

        token_mint_key = Pubkey.from_string(listing.tokenMint)
        metadata_account = derive_metadata_key(token_mint_key)
        auction_house_key = Pubkey.from_string(listing.auctionHouse)
        notary_key = self.me_v2_notary
        seller_key =Pubkey.from_string(listing.seller)

        program_as_signer_key, program_as_signer_bump = Pubkey.find_program_address(
            seeds=[
              b"m2",
              b"signer",
            ], 
            program_id=self.me_v2_program_id
        )

        # Get associated token account
        token_account_key = Pubkey.from_string(listing.tokenAddress)
        logger.info(f"Calculated Token Account: {token_account_key}")

        # Get associated token account
        buyer_token_account_key = get_associated_token_address(
            owner=wallet.pubkey(),
            mint=token_mint_key
        )

        escrow_payment_account, escrow_payment_bump = Pubkey.find_program_address(
            seeds=[
                b"m2",
                bytes(auction_house_key),
                bytes(wallet.pubkey()),
            ],
            program_id=self.me_v2_program_id,
        )
        logger.info(f"Calculated Escrow Payment Account: {escrow_payment_account}")

        auction_house_treasury_key, _ = Pubkey.find_program_address(
            seeds=[
                b"m2",
                bytes(auction_house_key),
                b"treasury",
            ],
            program_id=self.me_v2_program_id,
        )
        logger.info(f"Calculated Auction house Treasury: {auction_house_treasury_key}")

        buyer_trade_state, _ = Pubkey.find_program_address(
            seeds=[
                b"m2",
                bytes(wallet.pubkey()),
                bytes(auction_house_key),
                bytes(token_mint_key),
            ],
            program_id=self.me_v2_program_id,
        )
        logger.info(f"Calculated Buyer Trade State: {buyer_trade_state}")

        seller_trade_state, _ = Pubkey.find_program_address(
            seeds=[
                b"m2",
                bytes(seller_key),  # Replace with actual seller pubkey
                bytes(auction_house_key),
                bytes(token_account_key),
                bytes(token_mint_key),
            ],
            program_id=self.me_v2_program_id
        )
        logger.info(f"Calculated Seller Trade State: {seller_trade_state}")

        accounts = [
            AccountMeta(pubkey=wallet.pubkey(), is_signer=True, is_writable=True),
            AccountMeta(pubkey=seller_key, is_signer=False, is_writable=True),  # Seller account
            AccountMeta(pubkey=notary_key, is_signer=False, is_writable=False),
            AccountMeta(pubkey=token_account_key, is_signer=False, is_writable=True), # token account
            AccountMeta(pubkey=token_mint_key, is_signer=False, is_writable=False),
            AccountMeta(pubkey=metadata_account, is_signer=False, is_writable=False),
            AccountMeta(pubkey=escrow_payment_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=buyer_token_account_key, is_signer=False, is_writable=True), # Buyer receipt token account
            AccountMeta(pubkey=self.me_v2_authority, is_signer=False, is_writable=False), # Authority
            AccountMeta(pubkey=auction_house_key, is_signer=False, is_writable=False),
            AccountMeta(pubkey=auction_house_treasury_key, is_signer=False, is_writable=True),
            AccountMeta(pubkey=buyer_trade_state, is_signer=False, is_writable=True),
            AccountMeta(pubkey=self.me_v2_authority, is_signer=False, is_writable=True),
            AccountMeta(pubkey=seller_trade_state, is_signer=False, is_writable=True),
            AccountMeta(pubkey=self.me_v2_authority, is_signer=False, is_writable=True),
            AccountMeta(pubkey=self.token_program, is_signer=False, is_writable=False),
            AccountMeta(pubkey=self.system_program, is_signer=False, is_writable=False),
            AccountMeta(pubkey=self.ata_program, is_signer=False, is_writable=False), # ATA program
            AccountMeta(pubkey=program_as_signer_key, is_signer=False, is_writable=False),
            AccountMeta(pubkey=self.rent_program, is_signer=False, is_writable=False), # Rent Sysvar
        ]
        
        logger.info("Accounts details:")
        for i, account in enumerate(accounts):
            logger.info(f"Account {i + 1}: pubkey={account.pubkey}, is_signer={account.is_signer}, is_writable={account.is_writable}")

        identifier = b'[\xdc1\xdf\xcc\x815\xc1'  # Identifier for executeSaleV2 instruction
        instruction_data = ExecuteSaleInstruction.layout.build({
            "escrow_payment_bump": escrow_payment_bump,
            "program_as_signer_bump": program_as_signer_bump,
            "buyer_price": price_lamports,
            "token_size": 1,
            "buyer_state_expiry": 0,
            "seller_state_expiry": 0,
            "maker_fee_bp": 0,
            "taker_fee_bp": 0
        })
        data = identifier + instruction_data
        logger.info(f"Instruction data (hex): {data.hex()}")

        instruction = Instruction(
            program_id=self.me_v2_program_id,
            data=data,
            accounts=accounts,
        )

        return instruction

    async def _create_core_execute_sale_instruction(self, wallet: Keypair, listing: NFTListing, price_lamports: int) -> Instruction:
        """Creates instruction for buying MPL Core NFT according to IDL"""
        logger.info("Building core_execute_sale_v2 instruction")

        # Get account keys
        token_mint_key = Pubkey.from_string(listing.tokenMint)
        token_account_key = Pubkey.from_string(listing.tokenAddress)
        auction_house_key = Pubkey.from_string(listing.auctionHouse)
        seller_key = Pubkey.from_string(listing.seller)
        notary_key = self.me_v2_notary
        collection_key = Pubkey.from_string(listing.token.updateAuthority)

        # Derive PDAs
        program_as_signer_key, _ = Pubkey.find_program_address(
            seeds=[b"m2", b"signer"], 
            program_id=self.me_v2_program_id
        )

        escrow_payment_account, _ = Pubkey.find_program_address(
            seeds=[b"m2", bytes(auction_house_key), bytes(wallet.pubkey())],
            program_id=self.me_v2_program_id
        )

        auction_house_treasury_key, _ = Pubkey.find_program_address(
            seeds=[b"m2", bytes(auction_house_key), b"treasury"],
            program_id=self.me_v2_program_id
        )

        buyer_trade_state, _ = Pubkey.find_program_address(
            seeds=[b"m2", bytes(wallet.pubkey()), bytes(auction_house_key), bytes(token_mint_key)],
            program_id=self.me_v2_program_id
        )

        seller_trade_state, _ = Pubkey.find_program_address(
            seeds=[
                b"m2",
                bytes(seller_key),  # Replace with actual seller pubkey
                bytes(auction_house_key),
                bytes(token_account_key),
                bytes(token_mint_key),
            ],
            program_id=self.me_v2_program_id
        )
        logger.info(f"Calculated Seller Trade State: {seller_trade_state}")

        # Build accounts array according to IDL order
        accounts = [
            AccountMeta(pubkey=wallet.pubkey(), is_signer=True, is_writable=True),         # payer
            AccountMeta(pubkey=wallet.pubkey(), is_signer=False, is_writable=True),        # buyer
            AccountMeta(pubkey=seller_key, is_signer=False, is_writable=True),             # seller
            AccountMeta(pubkey=notary_key, is_signer=False, is_writable=False),            # notary
            AccountMeta(pubkey=program_as_signer_key, is_signer=False, is_writable=False), # programAsSigner
            AccountMeta(pubkey=token_mint_key, is_signer=False, is_writable=True),         # asset
            AccountMeta(pubkey=auction_house_key, is_signer=False, is_writable=False),      # auctionHouse
            AccountMeta(pubkey=auction_house_treasury_key, is_signer=False, is_writable=True), # auctionHouseTreasury
            AccountMeta(pubkey=seller_trade_state, is_signer=False, is_writable=True),      # sellerTradeState
            AccountMeta(pubkey=buyer_trade_state, is_signer=False, is_writable=True),       # buyerTradeState
            AccountMeta(pubkey=escrow_payment_account, is_signer=False, is_writable=True),  # buyerEscrowPaymentAccount
            AccountMeta(pubkey=self.me_v2_authority, is_signer=False, is_writable=False),   # buyerReferral
            AccountMeta(pubkey=self.me_v2_authority, is_signer=False, is_writable=False),   # sellerReferral
            AccountMeta(pubkey=self.mpl_core_program, is_signer=False, is_writable=False),  # assetProgram
            AccountMeta(pubkey=self.system_program, is_signer=False, is_writable=False),    # systemProgram
            AccountMeta(pubkey=collection_key, is_signer=False, is_writable=False),         # collection
            AccountMeta(pubkey=self.system_program, is_signer=False, is_writable=False),         # paymentMint 
            AccountMeta(pubkey=self.system_program, is_signer=False, is_writable=False),    # paymentSourceTokenAccount (native SOL)
            AccountMeta(pubkey=self.system_program, is_signer=False, is_writable=False),    # paymentSellerTokenAccount (native SOL)
            AccountMeta(pubkey=self.system_program, is_signer=False, is_writable=False),    # paymentTreasuryTokenAccount
            AccountMeta(pubkey=self.token_program, is_signer=False, is_writable=False),     # paymentTokenProgram
        ]

        # Add creator accounts if present
        if listing.token.properties.creators:
            for creator in listing.token.properties.creators:
                creator_key = Pubkey.from_string(creator["address"])
                accounts.append(AccountMeta(pubkey=creator_key, is_signer=False, is_writable=True))

        logger.info("Accounts details:")
        for i, account in enumerate(accounts):
            logger.info(f"Account {i + 1}: pubkey={account.pubkey}, is_signer={account.is_signer}, is_writable={account.is_writable}")

        identifier = b'\xd5b\xc5\x18\xf25\x9a#'
        instruction_data = CoreBuyInstruction.layout.build({
            "price": price_lamports,
            "maker_fee_bp": 0,
            "taker_fee_bp": 0,
            "compression_proof": None
        })
        data = identifier + instruction_data
        logger.info(f"Instruction data (hex): {data.hex()}")

        return Instruction(
            program_id=self.me_v2_program_id,
            data=data,
            accounts=accounts
        )
    
    async def buy_nft(
        self,
        wallet: Keypair,
        token_mint: str,
    ) -> str:
        try:
            logger.info(f"Starting NFT purchase process for mint: {token_mint}")
            
            listing = await self.get_listing_info(token_mint)
            logger.info(f"Listing received: {listing}")  # Add this line

            price_lamports = int(float(listing.price) * 1_000_000_000)
            
            logger.info(f"Building transaction for NFT: {listing.token.name}")
            logger.info(f"Price: {listing.price} SOL ({price_lamports} lamports)")
            
            # Check if NFT is MPL Core
            is_mpl_core = await self.is_mpl_core_nft(token_mint)
            token_program = self.token_program if not is_mpl_core else self.mpl_core_program
            logger.info(f"is_mpl_core {is_mpl_core}")

            tx = Transaction()
            tx.fee_payer = wallet.pubkey()

            set_compute_unit_limit_ix = set_compute_unit_limit(300000)
            tx.add(set_compute_unit_limit_ix)

            set_compute_unit_price_ix = set_compute_unit_price(30000)
            tx.add(set_compute_unit_price_ix)
            
            logger.info("Add deposit instruction")
            deposit_instruction = self._create_deposit_instruction(wallet, listing, price_lamports)
            tx.add(deposit_instruction)

            logger.info("Add buy_v2 instruction")
            buy_instruction = self._create_buy_instruction(wallet, listing, price_lamports, token_program)
            tx.add(buy_instruction)

            logger.info("Add execute_sale_v2 instruction")
            # Add appropriate execute sale instruction based on NFT type
            if is_mpl_core:
                execute_ix = await self._create_core_execute_sale_instruction(wallet, listing, price_lamports)
            else:
                execute_ix = self._create_execute_sale_instruction(wallet, listing, price_lamports)
            tx.add(execute_ix)

            logger.info("Sending transaction with retry mechanism")
            tx_signature = await self.send_and_confirm_transaction(tx, wallet)
            
            logger.info(f"NFT purchase successful! Transaction signature: {tx_signature}")
            return tx_signature

        except Exception as e:
            error_trace = traceback.format_exc()
            print(f"Error transferring NFT:\n{error_trace}")
            error_msg = f"Failed to buy NFT: {str(e)}"
            logger.error(error_msg)
            raise ConnectionError(error_msg)

async def buy_nft(
    buyer_private_key: str,
    token_mint: str,
) -> str:
    logger.info(f"Initiating NFT purchase for mint: {token_mint}")
    
    try:
        service = NFTBuyingService()
        wallet = Keypair.from_base58_string(buyer_private_key)
        
        result = await service.buy_nft(
            wallet=wallet,
            token_mint=token_mint
        )
        
        logger.info(f"NFT purchase completed. Transaction signature: {result}")
        return result
        
    except Exception as e:
        logger.red(f"NFT purchase failed: {str(e)}")
        raise