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


class UtilizeArgs(typing.TypedDict):
    utilize_args: types.utilize_args.UtilizeArgs


layout = borsh.CStruct("utilize_args" / types.utilize_args.UtilizeArgs.layout)


class UtilizeAccounts(typing.TypedDict):
    metadata: Pubkey
    token_account: Pubkey
    mint: Pubkey
    use_authority: Pubkey
    owner: Pubkey
    ata_program: Pubkey
    use_authority_record: typing.Optional[Pubkey]
    burner: typing.Optional[Pubkey]


def utilize(
    args: UtilizeArgs,
    accounts: UtilizeAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["use_authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["owner"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["ata_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["use_authority_record"], is_signer=False, is_writable=True
        )
        if accounts["use_authority_record"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["burner"], is_signer=False, is_writable=False)
        if accounts["burner"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"h\x92\xf2\xd1\xb0\xae\xb9\xa3"
    encoded_args = layout.build(
        {
            "utilize_args": args["utilize_args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
