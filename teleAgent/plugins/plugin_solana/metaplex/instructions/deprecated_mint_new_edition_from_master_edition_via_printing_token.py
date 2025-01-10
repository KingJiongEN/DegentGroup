from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class DeprecatedMintNewEditionFromMasterEditionViaPrintingTokenAccounts(
    typing.TypedDict
):
    metadata: Pubkey
    edition: Pubkey
    master_edition: Pubkey
    mint: Pubkey
    mint_authority: Pubkey
    printing_mint: Pubkey
    master_token_account: Pubkey
    edition_marker: Pubkey
    burn_authority: Pubkey
    payer: Pubkey
    master_update_authority: Pubkey
    master_metadata: Pubkey
    reservation_list: typing.Optional[Pubkey]


def deprecated_mint_new_edition_from_master_edition_via_printing_token(
    accounts: DeprecatedMintNewEditionFromMasterEditionViaPrintingTokenAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["edition"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["master_edition"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["mint_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["printing_mint"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["master_token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["edition_marker"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["burn_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["master_update_authority"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["master_metadata"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["reservation_list"], is_signer=False, is_writable=True
        )
        if accounts["reservation_list"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x9a$\xaeo\xbeP\x9b\xe4"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
