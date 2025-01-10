import typing
from dataclasses import dataclass
from construct import Construct
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


class ReservationListV1JSON(typing.TypedDict):
    key: types.key.KeyJSON
    master_edition: str
    supply_snapshot: typing.Optional[int]
    reservations: list[types.reservation_v1.ReservationV1JSON]


@dataclass
class ReservationListV1:
    discriminator: typing.ClassVar = b"\xefO\x0c\xcet\x99\x01\x8c"
    layout: typing.ClassVar = borsh.CStruct(
        "key" / types.key.layout,
        "master_edition" / BorshPubkey,
        "supply_snapshot" / borsh.Option(borsh.U64),
        "reservations"
        / borsh.Vec(typing.cast(Construct, types.reservation_v1.ReservationV1.layout)),
    )
    key: types.key.KeyKind
    master_edition: Pubkey
    supply_snapshot: typing.Optional[int]
    reservations: list[types.reservation_v1.ReservationV1]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["ReservationListV1"]:
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
    ) -> typing.List[typing.Optional["ReservationListV1"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ReservationListV1"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ReservationListV1":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = ReservationListV1.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            key=types.key.from_decoded(dec.key),
            master_edition=dec.master_edition,
            supply_snapshot=dec.supply_snapshot,
            reservations=list(
                map(
                    lambda item: types.reservation_v1.ReservationV1.from_decoded(item),
                    dec.reservations,
                )
            ),
        )

    def to_json(self) -> ReservationListV1JSON:
        return {
            "key": self.key.to_json(),
            "master_edition": str(self.master_edition),
            "supply_snapshot": self.supply_snapshot,
            "reservations": list(map(lambda item: item.to_json(), self.reservations)),
        }

    @classmethod
    def from_json(cls, obj: ReservationListV1JSON) -> "ReservationListV1":
        return cls(
            key=types.key.from_json(obj["key"]),
            master_edition=Pubkey.from_string(obj["master_edition"]),
            supply_snapshot=obj["supply_snapshot"],
            reservations=list(
                map(
                    lambda item: types.reservation_v1.ReservationV1.from_json(item),
                    obj["reservations"],
                )
            ),
        )
