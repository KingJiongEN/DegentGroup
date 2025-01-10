from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class MintArgs(typing.TypedDict):
    mint_args: types.mint_args.MintArgsKind


layout = borsh.CStruct("mint_args" / types.mint_args.layout)


class MintAccounts(typing.TypedDict):
    token: Pubkey
    token_owner: typing.Optional[Pubkey]
    metadata: Pubkey
    master_edition: typing.Optional[Pubkey]
    token_record: typing.Optional[Pubkey]
    mint: Pubkey
    authority: Pubkey
    delegate_record: typing.Optional[Pubkey]
    payer: Pubkey
    sysvar_instructions: Pubkey
    spl_token_program: Pubkey
    spl_ata_program: Pubkey
    authorization_rules_program: typing.Optional[Pubkey]
    authorization_rules: typing.Optional[Pubkey]


def mint(
    args: MintArgs,
    accounts: MintAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["token"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["token_owner"], is_signer=False, is_writable=False)
        if accounts["token_owner"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["master_edition"], is_signer=False, is_writable=True
        )
        if accounts["master_edition"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["token_record"], is_signer=False, is_writable=True)
        if accounts["token_record"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["delegate_record"], is_signer=False, is_writable=False
        )
        if accounts["delegate_record"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
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
    identifier = b"39\xe1/\xb6\x92\x89\xa6"
    encoded_args = layout.build(
        {
            "mint_args": args["mint_args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
