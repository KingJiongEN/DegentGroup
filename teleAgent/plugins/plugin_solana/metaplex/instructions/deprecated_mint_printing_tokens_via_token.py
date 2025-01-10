from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class DeprecatedMintPrintingTokensViaTokenAccounts(typing.TypedDict):
    destination: Pubkey
    token: Pubkey
    one_time_printing_authorization_mint: Pubkey
    printing_mint: Pubkey
    burn_authority: Pubkey
    metadata: Pubkey
    master_edition: Pubkey


def deprecated_mint_printing_tokens_via_token(
    accounts: DeprecatedMintPrintingTokensViaTokenAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["destination"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["token"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["one_time_printing_authorization_mint"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["printing_mint"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["burn_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["master_edition"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b'T"\x98\x85\x910\x04\xdf'
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
