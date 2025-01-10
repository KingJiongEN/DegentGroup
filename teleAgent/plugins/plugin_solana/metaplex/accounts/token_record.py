import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID
from .. import types


class TokenRecordJSON(typing.TypedDict):
    key: types.key.KeyJSON
    bump: int
    state: types.token_state.TokenStateJSON
    rule_set_revision: typing.Optional[int]
    delegate: typing.Optional[str]
    delegate_role: typing.Optional[types.token_delegate_role.TokenDelegateRoleJSON]
    locked_transfer: typing.Optional[str]


@dataclass
class TokenRecord:
    discriminator: typing.ClassVar = b"\x1b\xbb d\x89\xfdh\xf2"
    layout: typing.ClassVar = borsh.CStruct(
        "key" / types.key.layout,
        "bump" / borsh.U8,
        "state" / types.token_state.layout,
        "rule_set_revision" / borsh.Option(borsh.U64),
        "delegate" / borsh.Option(BorshPubkey),
        "delegate_role" / borsh.Option(types.token_delegate_role.layout),
        "locked_transfer" / borsh.Option(BorshPubkey),
    )
    key: types.key.KeyKind
    bump: int
    state: types.token_state.TokenStateKind
    rule_set_revision: typing.Optional[int]
    delegate: typing.Optional[Pubkey]
    delegate_role: typing.Optional[types.token_delegate_role.TokenDelegateRoleKind]
    locked_transfer: typing.Optional[Pubkey]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["TokenRecord"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp.value
        if info is None:
            return None
        if info.owner != program_id:
            raise ValueError("Account does not belong to this program")
        bytes_data = info.data
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[Pubkey],
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.List[typing.Optional["TokenRecord"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["TokenRecord"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "TokenRecord":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = TokenRecord.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            key=types.key.from_decoded(dec.key),
            bump=dec.bump,
            state=types.token_state.from_decoded(dec.state),
            rule_set_revision=dec.rule_set_revision,
            delegate=dec.delegate,
            delegate_role=(
                None
                if dec.delegate_role is None
                else types.token_delegate_role.from_decoded(dec.delegate_role)
            ),
            locked_transfer=dec.locked_transfer,
        )

    def to_json(self) -> TokenRecordJSON:
        return {
            "key": self.key.to_json(),
            "bump": self.bump,
            "state": self.state.to_json(),
            "rule_set_revision": self.rule_set_revision,
            "delegate": (None if self.delegate is None else str(self.delegate)),
            "delegate_role": (
                None if self.delegate_role is None else self.delegate_role.to_json()
            ),
            "locked_transfer": (
                None if self.locked_transfer is None else str(self.locked_transfer)
            ),
        }

    @classmethod
    def from_json(cls, obj: TokenRecordJSON) -> "TokenRecord":
        return cls(
            key=types.key.from_json(obj["key"]),
            bump=obj["bump"],
            state=types.token_state.from_json(obj["state"]),
            rule_set_revision=obj["rule_set_revision"],
            delegate=(
                None if obj["delegate"] is None else Pubkey.from_string(obj["delegate"])
            ),
            delegate_role=(
                None
                if obj["delegate_role"] is None
                else types.token_delegate_role.from_json(obj["delegate_role"])
            ),
            locked_transfer=(
                None
                if obj["locked_transfer"] is None
                else Pubkey.from_string(obj["locked_transfer"])
            ),
        )
