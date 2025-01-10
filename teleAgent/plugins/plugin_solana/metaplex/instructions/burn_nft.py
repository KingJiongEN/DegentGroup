from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class BurnNftAccounts(typing.TypedDict):
    metadata: Pubkey
    owner: Pubkey
    mint: Pubkey
    token_account: Pubkey
    master_edition_account: Pubkey
    spl_token_program: Pubkey
    collection_metadata: typing.Optional[Pubkey]


def burn_nft(
    accounts: BurnNftAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["owner"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["master_edition_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["spl_token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["collection_metadata"], is_signer=False, is_writable=True
        )
        if accounts["collection_metadata"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"w\r\xb7\x11\xc2\xf3&\x1f"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
