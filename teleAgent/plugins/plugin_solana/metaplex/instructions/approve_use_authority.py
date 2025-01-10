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


class ApproveUseAuthorityArgs(typing.TypedDict):
    approve_use_authority_args: types.approve_use_authority_args.ApproveUseAuthorityArgs


layout = borsh.CStruct(
    "approve_use_authority_args"
    / types.approve_use_authority_args.ApproveUseAuthorityArgs.layout
)


class ApproveUseAuthorityAccounts(typing.TypedDict):
    use_authority_record: Pubkey
    owner: Pubkey
    payer: Pubkey
    user: Pubkey
    owner_token_account: Pubkey
    metadata: Pubkey
    mint: Pubkey
    burner: Pubkey


def approve_use_authority(
    args: ApproveUseAuthorityArgs,
    accounts: ApproveUseAuthorityAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["use_authority_record"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["owner"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["user"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["owner_token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["burner"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False)
        if RENT
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x0e\x04M\x86V\x17%\xec"
    encoded_args = layout.build(
        {
            "approve_use_authority_args": args[
                "approve_use_authority_args"
            ].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
