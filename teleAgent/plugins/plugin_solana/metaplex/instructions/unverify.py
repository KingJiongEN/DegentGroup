from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class UnverifyArgs(typing.TypedDict):
    verification_args: types.verification_args.VerificationArgsKind


layout = borsh.CStruct("verification_args" / types.verification_args.layout)


class UnverifyAccounts(typing.TypedDict):
    authority: Pubkey
    delegate_record: typing.Optional[Pubkey]
    metadata: Pubkey
    collection_mint: typing.Optional[Pubkey]
    collection_metadata: typing.Optional[Pubkey]
    sysvar_instructions: Pubkey


def unverify(
    args: UnverifyArgs,
    accounts: UnverifyAccounts,
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
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["collection_mint"], is_signer=False, is_writable=False
        )
        if accounts["collection_mint"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["collection_metadata"], is_signer=False, is_writable=True
        )
        if accounts["collection_metadata"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["sysvar_instructions"], is_signer=False, is_writable=False
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"7\x01\x19XsC\x14\x18"
    encoded_args = layout.build(
        {
            "verification_args": args["verification_args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
