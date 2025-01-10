from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class PuffMetadataAccounts(typing.TypedDict):
    metadata: Pubkey


def puff_metadata(
    accounts: PuffMetadataAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True)
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"W\xd9\x15\x84i\xeeGr"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
