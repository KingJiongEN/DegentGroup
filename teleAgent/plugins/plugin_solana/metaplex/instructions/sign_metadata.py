from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class SignMetadataAccounts(typing.TypedDict):
    metadata: Pubkey
    creator: Pubkey


def sign_metadata(
    accounts: SignMetadataAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["creator"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xb2\xf5\xfd\xcd\xec\xfa\xe9\xd1"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
