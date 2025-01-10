from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class MigrateAccounts(typing.TypedDict):
    metadata: Pubkey
    edition: Pubkey
    token: Pubkey
    token_owner: Pubkey
    mint: Pubkey
    payer: Pubkey
    authority: Pubkey
    collection_metadata: Pubkey
    delegate_record: Pubkey
    token_record: Pubkey
    sysvar_instructions: Pubkey
    spl_token_program: Pubkey
    authorization_rules_program: typing.Optional[Pubkey]
    authorization_rules: typing.Optional[Pubkey]


def migrate(
    accounts: MigrateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["edition"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["token"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["token_owner"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["collection_metadata"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["delegate_record"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["token_record"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["sysvar_instructions"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["spl_token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["authorization_rules_program"],
            is_signer=False,
            is_writable=False,
        )
        if accounts["authorization_rules_program"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["authorization_rules"], is_signer=False, is_writable=False
        )
        if accounts["authorization_rules"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x9b\xea\xe7\x92\xec\x9e\xa2\x1e"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
