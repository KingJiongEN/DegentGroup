from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class RevokeCollectionAuthorityAccounts(typing.TypedDict):
    collection_authority_record: Pubkey
    delegate_authority: Pubkey
    revoke_authority: Pubkey
    metadata: Pubkey
    mint: Pubkey


def revoke_collection_authority(
    accounts: RevokeCollectionAuthorityAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["collection_authority_record"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["delegate_authority"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["revoke_authority"], is_signer=True, is_writable=True
        ),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x1f\x8b\x87\xc6\x1d0\xa0\x9a"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
