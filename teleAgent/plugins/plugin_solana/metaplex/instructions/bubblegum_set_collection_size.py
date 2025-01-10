from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class BubblegumSetCollectionSizeArgs(typing.TypedDict):
    set_collection_size_args: types.set_collection_size_args.SetCollectionSizeArgs


layout = borsh.CStruct(
    "set_collection_size_args"
    / types.set_collection_size_args.SetCollectionSizeArgs.layout
)


class BubblegumSetCollectionSizeAccounts(typing.TypedDict):
    collection_metadata: Pubkey
    collection_authority: Pubkey
    collection_mint: Pubkey
    bubblegum_signer: Pubkey
    collection_authority_record: typing.Optional[Pubkey]


def bubblegum_set_collection_size(
    args: BubblegumSetCollectionSizeArgs,
    accounts: BubblegumSetCollectionSizeAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["collection_metadata"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["collection_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["collection_mint"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["bubblegum_signer"], is_signer=True, is_writable=False
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
    identifier = b"\xe6\xd7\xe7\xe2\x9c\xbc8\x06"
    encoded_args = layout.build(
        {
            "set_collection_size_args": args["set_collection_size_args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
