from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class SetTokenStandardAccounts(typing.TypedDict):
    metadata: Pubkey
    update_authority: Pubkey
    mint: Pubkey
    edition: typing.Optional[Pubkey]


def set_token_standard(
    accounts: SetTokenStandardAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["update_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["edition"], is_signer=False, is_writable=False)
        if accounts["edition"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x93\xd4j\xc3\x1e\xaa\xd1\x80"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
