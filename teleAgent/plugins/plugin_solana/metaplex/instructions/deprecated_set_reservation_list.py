from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class DeprecatedSetReservationListAccounts(typing.TypedDict):
    master_edition: Pubkey
    reservation_list: Pubkey
    resource: Pubkey


def deprecated_set_reservation_list(
    accounts: DeprecatedSetReservationListAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["master_edition"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["reservation_list"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["resource"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"D\x1cB\x13;\xcb\xbe\x8e"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
