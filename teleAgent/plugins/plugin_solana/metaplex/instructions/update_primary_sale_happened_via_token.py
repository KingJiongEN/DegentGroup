from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class UpdatePrimarySaleHappenedViaTokenAccounts(typing.TypedDict):
    metadata: Pubkey
    owner: Pubkey
    token: Pubkey


def update_primary_sale_happened_via_token(
    accounts: UpdatePrimarySaleHappenedViaTokenAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["owner"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["token"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xac\x81\xad\xd2\xde\x81\xf3b"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
