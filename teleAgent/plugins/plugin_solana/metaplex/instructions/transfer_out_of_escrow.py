from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class TransferOutOfEscrowArgs(typing.TypedDict):
    transfer_out_of_escrow_args: types.transfer_out_of_escrow_args.TransferOutOfEscrowArgs


layout = borsh.CStruct(
    "transfer_out_of_escrow_args"
    / types.transfer_out_of_escrow_args.TransferOutOfEscrowArgs.layout
)


class TransferOutOfEscrowAccounts(typing.TypedDict):
    escrow: Pubkey
    metadata: Pubkey
    payer: Pubkey
    attribute_mint: Pubkey
    attribute_src: Pubkey
    attribute_dst: Pubkey
    escrow_mint: Pubkey
    escrow_account: Pubkey
    ata_program: Pubkey
    sysvar_instructions: Pubkey
    authority: typing.Optional[Pubkey]


def transfer_out_of_escrow(
    args: TransferOutOfEscrowArgs,
    accounts: TransferOutOfEscrowAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["escrow"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["attribute_mint"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["attribute_src"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["attribute_dst"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["escrow_mint"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["escrow_account"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["ata_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["sysvar_instructions"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False)
        if accounts["authority"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"7\xba\xba\xd8s\x9e:\x99"
    encoded_args = layout.build(
        {
            "transfer_out_of_escrow_args": args[
                "transfer_out_of_escrow_args"
            ].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
