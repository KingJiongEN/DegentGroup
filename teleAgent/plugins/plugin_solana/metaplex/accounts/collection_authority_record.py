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


class CollectionAuthorityRecordJSON(typing.TypedDict):
    key: types.key.KeyJSON
    bump: int
    update_authority: typing.Optional[str]


@dataclass
class CollectionAuthorityRecord:
    discriminator: typing.ClassVar = b"\x9c0l\x1f\xd4\xdbd\xa8"
    layout: typing.ClassVar = borsh.CStruct(
        "key" / types.key.layout,
        "bump" / borsh.U8,
        "update_authority" / borsh.Option(BorshPubkey),
    )
    key: types.key.KeyKind
    bump: int
    update_authority: typing.Optional[Pubkey]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["CollectionAuthorityRecord"]:
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
    ) -> typing.List[typing.Optional["CollectionAuthorityRecord"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["CollectionAuthorityRecord"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "CollectionAuthorityRecord":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = CollectionAuthorityRecord.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            key=types.key.from_decoded(dec.key),
            bump=dec.bump,
            update_authority=dec.update_authority,
        )

    def to_json(self) -> CollectionAuthorityRecordJSON:
        return {
            "key": self.key.to_json(),
            "bump": self.bump,
            "update_authority": (
                None if self.update_authority is None else str(self.update_authority)
            ),
        }

    @classmethod
    def from_json(
        cls, obj: CollectionAuthorityRecordJSON
    ) -> "CollectionAuthorityRecord":
        return cls(
            key=types.key.from_json(obj["key"]),
            bump=obj["bump"],
            update_authority=(
                None
                if obj["update_authority"] is None
                else Pubkey.from_string(obj["update_authority"])
            ),
        )
