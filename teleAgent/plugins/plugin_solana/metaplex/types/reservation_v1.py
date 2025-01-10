from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class ReservationV1JSON(typing.TypedDict):
    address: str
    spots_remaining: int
    total_spots: int


@dataclass
class ReservationV1:
    layout: typing.ClassVar = borsh.CStruct(
        "address" / BorshPubkey, "spots_remaining" / borsh.U8, "total_spots" / borsh.U8
    )
    address: Pubkey
    spots_remaining: int
    total_spots: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "ReservationV1":
        return cls(
            address=obj.address,
            spots_remaining=obj.spots_remaining,
            total_spots=obj.total_spots,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "address": self.address,
            "spots_remaining": self.spots_remaining,
            "total_spots": self.total_spots,
        }

    def to_json(self) -> ReservationV1JSON:
        return {
            "address": str(self.address),
            "spots_remaining": self.spots_remaining,
            "total_spots": self.total_spots,
        }

    @classmethod
    def from_json(cls, obj: ReservationV1JSON) -> "ReservationV1":
        return cls(
            address=Pubkey.from_string(obj["address"]),
            spots_remaining=obj["spots_remaining"],
            total_spots=obj["total_spots"],
        )
