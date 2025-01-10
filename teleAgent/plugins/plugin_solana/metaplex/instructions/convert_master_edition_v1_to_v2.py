from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class ConvertMasterEditionV1ToV2Accounts(typing.TypedDict):
    master_edition: Pubkey
    one_time_auth: Pubkey
    printing_mint: Pubkey


def convert_master_edition_v1_to_v2(
    accounts: ConvertMasterEditionV1ToV2Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["master_edition"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["one_time_auth"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["printing_mint"], is_signer=False, is_writable=True
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xd9\x1al\x007~\xa7\xee"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
