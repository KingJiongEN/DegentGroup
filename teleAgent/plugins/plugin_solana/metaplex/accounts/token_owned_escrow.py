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


class TokenOwnedEscrowJSON(typing.TypedDict):
    key: types.key.KeyJSON
    base_token: str
    authority: types.escrow_authority.EscrowAuthorityJSON
    bump: int


@dataclass
class TokenOwnedEscrow:
    discriminator: typing.ClassVar = b"\x15\x89t[{b~\xe4"
    layout: typing.ClassVar = borsh.CStruct(
        "key" / types.key.layout,
        "base_token" / BorshPubkey,
        "authority" / types.escrow_authority.layout,
        "bump" / borsh.U8,
    )
    key: types.key.KeyKind
    base_token: Pubkey
    authority: types.escrow_authority.EscrowAuthorityKind
    bump: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["TokenOwnedEscrow"]:
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
    ) -> typing.List[typing.Optional["TokenOwnedEscrow"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["TokenOwnedEscrow"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "TokenOwnedEscrow":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = TokenOwnedEscrow.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            key=types.key.from_decoded(dec.key),
            base_token=dec.base_token,
            authority=types.escrow_authority.from_decoded(dec.authority),
            bump=dec.bump,
        )

    def to_json(self) -> TokenOwnedEscrowJSON:
        return {
            "key": self.key.to_json(),
            "base_token": str(self.base_token),
            "authority": self.authority.to_json(),
            "bump": self.bump,
        }

    @classmethod
    def from_json(cls, obj: TokenOwnedEscrowJSON) -> "TokenOwnedEscrow":
        return cls(
            key=types.key.from_json(obj["key"]),
            base_token=Pubkey.from_string(obj["base_token"]),
            authority=types.escrow_authority.from_json(obj["authority"]),
            bump=obj["bump"],
        )
