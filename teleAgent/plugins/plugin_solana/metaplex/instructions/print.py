from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class PrintArgs(typing.TypedDict):
    print_args: types.print_args.PrintArgsKind


layout = borsh.CStruct("print_args" / types.print_args.layout)


class PrintAccounts(typing.TypedDict):
    edition_metadata: Pubkey
    edition: Pubkey
    edition_mint: Pubkey
    edition_token_account_owner: Pubkey
    edition_token_account: Pubkey
    edition_mint_authority: Pubkey
    edition_token_record: typing.Optional[Pubkey]
    master_edition: Pubkey
    edition_marker_pda: Pubkey
    payer: Pubkey
    master_token_account_owner: Pubkey
    master_token_account: Pubkey
    master_metadata: Pubkey
    update_authority: Pubkey
    spl_token_program: Pubkey
    spl_ata_program: Pubkey
    sysvar_instructions: Pubkey


def print(
    args: PrintArgs,
    accounts: PrintAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["edition_metadata"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["edition"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["edition_mint"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["edition_token_account_owner"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["edition_token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["edition_mint_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["edition_token_record"], is_signer=False, is_writable=True
        )
        if accounts["edition_token_record"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["master_edition"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["edition_marker_pda"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["master_token_account_owner"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["master_token_account"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["master_metadata"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["update_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["spl_token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["spl_ata_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["sysvar_instructions"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xc3\xcf/LZ\xacsi"
    encoded_args = layout.build(
        {
            "print_args": args["print_args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
