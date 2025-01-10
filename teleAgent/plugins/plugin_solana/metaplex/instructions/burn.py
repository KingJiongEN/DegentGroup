from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class BurnArgs(typing.TypedDict):
    burn_args: types.burn_args.BurnArgsKind


layout = borsh.CStruct("burn_args" / types.burn_args.layout)


class BurnAccounts(typing.TypedDict):
    authority: Pubkey
    collection_metadata: typing.Optional[Pubkey]
    metadata: Pubkey
    edition: typing.Optional[Pubkey]
    mint: Pubkey
    token: Pubkey
    master_edition: typing.Optional[Pubkey]
    master_edition_mint: typing.Optional[Pubkey]
    master_edition_token: typing.Optional[Pubkey]
    edition_marker: typing.Optional[Pubkey]
    token_record: typing.Optional[Pubkey]
    sysvar_instructions: Pubkey
    spl_token_program: Pubkey


def burn(
    args: BurnArgs,
    accounts: BurnAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["collection_metadata"], is_signer=False, is_writable=True
        )
        if accounts["collection_metadata"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["edition"], is_signer=False, is_writable=True)
        if accounts["edition"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["token"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["master_edition"], is_signer=False, is_writable=True
        )
        if accounts["master_edition"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["master_edition_mint"], is_signer=False, is_writable=False
        )
        if accounts["master_edition_mint"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["master_edition_token"], is_signer=False, is_writable=False
        )
        if accounts["master_edition_token"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["edition_marker"], is_signer=False, is_writable=True
        )
        if accounts["edition_marker"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["token_record"], is_signer=False, is_writable=True)
        if accounts["token_record"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["sysvar_instructions"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["spl_token_program"], is_signer=False, is_writable=False
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"tn\x1d8k\xdb*]"
    encoded_args = layout.build(
        {
            "burn_args": args["burn_args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
