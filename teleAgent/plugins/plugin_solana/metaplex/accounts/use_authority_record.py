import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from ..program_id import PROGRAM_ID
from .. import types


class UseAuthorityRecordJSON(typing.TypedDict):
    key: types.key.KeyJSON
    allowed_uses: int
    bump: int


@dataclass
class UseAuthorityRecord:
    discriminator: typing.ClassVar = b"\xe3\xc8\xe6\xc5\xf4\xc6\xac2"
    layout: typing.ClassVar = borsh.CStruct(
        "key" / types.key.layout, "allowed_uses" / borsh.U64, "bump" / borsh.U8
    )
    key: types.key.KeyKind
    allowed_uses: int
    bump: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["UseAuthorityRecord"]:
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
    ) -> typing.List[typing.Optional["UseAuthorityRecord"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["UseAuthorityRecord"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "UseAuthorityRecord":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = UseAuthorityRecord.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            key=types.key.from_decoded(dec.key),
            allowed_uses=dec.allowed_uses,
            bump=dec.bump,
        )

    def to_json(self) -> UseAuthorityRecordJSON:
        return {
            "key": self.key.to_json(),
            "allowed_uses": self.allowed_uses,
            "bump": self.bump,
        }

    @classmethod
    def from_json(cls, obj: UseAuthorityRecordJSON) -> "UseAuthorityRecord":
        return cls(
            key=types.key.from_json(obj["key"]),
            allowed_uses=obj["allowed_uses"],
            bump=obj["bump"],
        )
