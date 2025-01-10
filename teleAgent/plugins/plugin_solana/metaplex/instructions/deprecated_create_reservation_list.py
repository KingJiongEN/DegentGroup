from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class DeprecatedCreateReservationListAccounts(typing.TypedDict):
    reservation_list: Pubkey
    payer: Pubkey
    update_authority: Pubkey
    master_edition: Pubkey
    resource: Pubkey
    metadata: Pubkey


def deprecated_create_reservation_list(
    accounts: DeprecatedCreateReservationListAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["reservation_list"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["update_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["master_edition"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["resource"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xab\xe3\xa1\x9e\x01\xb0iH"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
