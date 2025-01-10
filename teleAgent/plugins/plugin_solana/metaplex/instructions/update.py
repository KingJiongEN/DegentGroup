from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class UpdateArgs(typing.TypedDict):
    update_args: types.update_args.UpdateArgsKind


layout = borsh.CStruct("update_args" / types.update_args.layout)


class UpdateAccounts(typing.TypedDict):
    authority: Pubkey
    delegate_record: typing.Optional[Pubkey]
    token: typing.Optional[Pubkey]
    mint: Pubkey
    metadata: Pubkey
    edition: typing.Optional[Pubkey]
    payer: Pubkey
    sysvar_instructions: Pubkey
    authorization_rules_program: typing.Optional[Pubkey]
    authorization_rules: typing.Optional[Pubkey]


def update(
    args: UpdateArgs,
    accounts: UpdateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["delegate_record"], is_signer=False, is_writable=False
        )
        if accounts["delegate_record"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["token"], is_signer=False, is_writable=False)
        if accounts["token"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["edition"], is_signer=False, is_writable=False)
        if accounts["edition"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["sysvar_instructions"], is_signer=False, is_writable=False
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
    identifier = b"\xdb\xc8X\xb0\x9e?\xfd\x7f"
    encoded_args = layout.build(
        {
            "update_args": args["update_args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
