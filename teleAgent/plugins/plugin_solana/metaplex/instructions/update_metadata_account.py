from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class UpdateMetadataAccountAccounts(typing.TypedDict):
    metadata: Pubkey
    update_authority: Pubkey


def update_metadata_account(
    accounts: UpdateMetadataAccountAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["update_authority"], is_signer=True, is_writable=False
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x8d\x0e\x17h\xf7\xc05\xad"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
