from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class CollectAccounts(typing.TypedDict):
    authority: Pubkey
    recipient: Pubkey


def collect(
    accounts: CollectAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["recipient"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xd0/\xc2\x9b\x11bR\xec"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
