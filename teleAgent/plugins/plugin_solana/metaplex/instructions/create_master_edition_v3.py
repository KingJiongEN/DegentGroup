from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class CreateMasterEditionV3Args(typing.TypedDict):
    create_master_edition_args: types.create_master_edition_args.CreateMasterEditionArgs


layout = borsh.CStruct(
    "create_master_edition_args"
    / types.create_master_edition_args.CreateMasterEditionArgs.layout
)


class CreateMasterEditionV3Accounts(typing.TypedDict):
    edition: Pubkey
    mint: Pubkey
    update_authority: Pubkey
    mint_authority: Pubkey
    payer: Pubkey
    metadata: Pubkey


def create_master_edition_v3(
    args: CreateMasterEditionV3Args,
    accounts: CreateMasterEditionV3Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["edition"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["update_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["mint_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False)
        if RENT
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x93\x95\x11\x9fJ\x86r\xed"
    encoded_args = layout.build(
        {
            "create_master_edition_args": args[
                "create_master_edition_args"
            ].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
