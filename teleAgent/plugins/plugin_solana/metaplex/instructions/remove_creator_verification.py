from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class RemoveCreatorVerificationAccounts(typing.TypedDict):
    metadata: Pubkey
    creator: Pubkey


def remove_creator_verification(
    accounts: RemoveCreatorVerificationAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["creator"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b")\xc2\x8c\xd9Z\xa0\x8b\x06"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
