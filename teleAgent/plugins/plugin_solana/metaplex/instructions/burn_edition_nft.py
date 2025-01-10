from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class BurnEditionNftAccounts(typing.TypedDict):
    metadata: Pubkey
    owner: Pubkey
    print_edition_mint: Pubkey
    master_edition_mint: Pubkey
    print_edition_token_account: Pubkey
    master_edition_token_account: Pubkey
    master_edition_account: Pubkey
    print_edition_account: Pubkey
    edition_marker_account: Pubkey
    spl_token_program: Pubkey


def burn_edition_nft(
    accounts: BurnEditionNftAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["owner"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["print_edition_mint"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["master_edition_mint"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["print_edition_token_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["master_edition_token_account"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["master_edition_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["print_edition_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["edition_marker_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["spl_token_program"], is_signer=False, is_writable=False
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xddi\xc4@\xa4\x1b]\xc5"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
