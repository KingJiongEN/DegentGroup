from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class LockArgs(typing.TypedDict):
    lock_args: types.lock_args.LockArgsKind


layout = borsh.CStruct("lock_args" / types.lock_args.layout)


class LockAccounts(typing.TypedDict):
    authority: Pubkey
    token_owner: typing.Optional[Pubkey]
    token: Pubkey
    mint: Pubkey
    metadata: Pubkey
    edition: typing.Optional[Pubkey]
    token_record: typing.Optional[Pubkey]
    payer: Pubkey
    sysvar_instructions: Pubkey
    spl_token_program: typing.Optional[Pubkey]
    authorization_rules_program: typing.Optional[Pubkey]
    authorization_rules: typing.Optional[Pubkey]


def lock(
    args: LockArgs,
    accounts: LockAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["token_owner"], is_signer=False, is_writable=False)
        if accounts["token_owner"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["token"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["edition"], is_signer=False, is_writable=False)
        if accounts["edition"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["token_record"], is_signer=False, is_writable=True)
        if accounts["token_record"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["sysvar_instructions"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["spl_token_program"], is_signer=False, is_writable=False
        )
        if accounts["spl_token_program"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
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
    identifier = b"\x15\x13\xd0+\xed>\xffW"
    encoded_args = layout.build(
        {
            "lock_args": args["lock_args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
