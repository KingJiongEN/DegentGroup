from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class TransferArgs(typing.TypedDict):
    transfer_args: types.transfer_args.TransferArgsKind


layout = borsh.CStruct("transfer_args" / types.transfer_args.layout)


class TransferAccounts(typing.TypedDict):
    token: Pubkey
    token_owner: Pubkey
    destination: Pubkey
    destination_owner: Pubkey
    mint: Pubkey
    metadata: Pubkey
    edition: typing.Optional[Pubkey]
    owner_token_record: typing.Optional[Pubkey]
    destination_token_record: typing.Optional[Pubkey]
    authority: Pubkey
    payer: Pubkey
    sysvar_instructions: Pubkey
    spl_token_program: Pubkey
    spl_ata_program: Pubkey
    authorization_rules_program: typing.Optional[Pubkey]
    authorization_rules: typing.Optional[Pubkey]


def transfer(
    args: TransferArgs,
    accounts: TransferAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["token"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["token_owner"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["destination"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["destination_owner"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["edition"], is_signer=False, is_writable=False)
        if accounts["edition"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["owner_token_record"], is_signer=False, is_writable=True
        )
        if accounts["owner_token_record"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["destination_token_record"],
            is_signer=False,
            is_writable=True,
        )
        if accounts["destination_token_record"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["sysvar_instructions"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["spl_token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["spl_ata_program"], is_signer=False, is_writable=False
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
    identifier = b"\xa34\xc8\xe7\x8c\x03E\xba"
    encoded_args = layout.build(
        {
            "transfer_args": args["transfer_args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
