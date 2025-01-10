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


class MintNewEditionFromMasterEditionViaVaultProxyArgs(typing.TypedDict):
    mint_new_edition_from_master_edition_via_token_args: types.mint_new_edition_from_master_edition_via_token_args.MintNewEditionFromMasterEditionViaTokenArgs


layout = borsh.CStruct(
    "mint_new_edition_from_master_edition_via_token_args"
    / types.mint_new_edition_from_master_edition_via_token_args.MintNewEditionFromMasterEditionViaTokenArgs.layout
)


class MintNewEditionFromMasterEditionViaVaultProxyAccounts(typing.TypedDict):
    new_metadata: Pubkey
    new_edition: Pubkey
    master_edition: Pubkey
    new_mint: Pubkey
    edition_mark_pda: Pubkey
    new_mint_authority: Pubkey
    payer: Pubkey
    vault_authority: Pubkey
    safety_deposit_store: Pubkey
    safety_deposit_box: Pubkey
    vault: Pubkey
    new_metadata_update_authority: Pubkey
    metadata: Pubkey
    token_vault_program: Pubkey


def mint_new_edition_from_master_edition_via_vault_proxy(
    args: MintNewEditionFromMasterEditionViaVaultProxyArgs,
    accounts: MintNewEditionFromMasterEditionViaVaultProxyAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["new_metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["new_edition"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["master_edition"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["new_mint"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["edition_mark_pda"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["new_mint_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["vault_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["safety_deposit_store"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["safety_deposit_box"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["vault"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["new_metadata_update_authority"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["token_vault_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False)
        if RENT
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"B\xf6\xceI\xf9#\xc2/"
    encoded_args = layout.build(
        {
            "mint_new_edition_from_master_edition_via_token_args": args[
                "mint_new_edition_from_master_edition_via_token_args"
            ].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
