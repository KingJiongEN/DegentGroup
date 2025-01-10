from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class CreateMetadataAccountV3Args(typing.TypedDict):
    create_metadata_account_args_v3: types.create_metadata_account_args_v3.CreateMetadataAccountArgsV3


layout = borsh.CStruct(
    "create_metadata_account_args_v3"
    / types.create_metadata_account_args_v3.CreateMetadataAccountArgsV3.layout
)


class CreateMetadataAccountV3Accounts(typing.TypedDict):
    metadata: Pubkey
    mint: Pubkey
    mint_authority: Pubkey
    payer: Pubkey
    update_authority: Pubkey


def create_metadata_account_v3(
    args: CreateMetadataAccountV3Args,
    accounts: CreateMetadataAccountV3Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["mint_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["update_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False)
        if RENT
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"+\x0c\xaf\x0e\xfc-\xbc\x9b"
    encoded_args = layout.build(
        {
            "create_metadata_account_args_v3": args[
                "create_metadata_account_args_v3"
            ].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
