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


class EditionMarkerJSON(typing.TypedDict):
    key: types.key.KeyJSON
    ledger: list[int]


@dataclass
class EditionMarker:
    discriminator: typing.ClassVar = b"\xe9\n\x12\xe6\x81\xac%\xea"
    layout: typing.ClassVar = borsh.CStruct(
        "key" / types.key.layout, "ledger" / borsh.U8[31]
    )
    key: types.key.KeyKind
    ledger: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["EditionMarker"]:
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
    ) -> typing.List[typing.Optional["EditionMarker"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["EditionMarker"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "EditionMarker":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = EditionMarker.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            key=types.key.from_decoded(dec.key),
            ledger=dec.ledger,
        )

    def to_json(self) -> EditionMarkerJSON:
        return {
            "key": self.key.to_json(),
            "ledger": self.ledger,
        }

    @classmethod
    def from_json(cls, obj: EditionMarkerJSON) -> "EditionMarker":
        return cls(
            key=types.key.from_json(obj["key"]),
            ledger=obj["ledger"],
        )
