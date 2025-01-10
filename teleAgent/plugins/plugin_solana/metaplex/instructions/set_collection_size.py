from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SetCollectionSizeArgs(typing.TypedDict):
    set_collection_size_args: types.set_collection_size_args.SetCollectionSizeArgs


layout = borsh.CStruct(
    "set_collection_size_args"
    / types.set_collection_size_args.SetCollectionSizeArgs.layout
)


class SetCollectionSizeAccounts(typing.TypedDict):
    collection_metadata: Pubkey
    collection_authority: Pubkey
    collection_mint: Pubkey
    collection_authority_record: typing.Optional[Pubkey]


def set_collection_size(
    args: SetCollectionSizeArgs,
    accounts: SetCollectionSizeAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["collection_metadata"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["collection_authority"], is_signer=True, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["collection_mint"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["collection_authority_record"],
            is_signer=False,
            is_writable=False,
        )
        if accounts["collection_authority_record"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x9d\xfe\xa6\x90+\xdf\xc7'"
    encoded_args = layout.build(
        {
            "set_collection_size_args": args["set_collection_size_args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
