from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class CreatorJSON(typing.TypedDict):
    address: str
    verified: bool
    share: int


@dataclass
class Creator:
    layout: typing.ClassVar = borsh.CStruct(
        "address" / BorshPubkey, "verified" / borsh.Bool, "share" / borsh.U8
    )
    address: Pubkey
    verified: bool
    share: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "Creator":
        return cls(address=obj.address, verified=obj.verified, share=obj.share)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"address": self.address, "verified": self.verified, "share": self.share}

    def to_json(self) -> CreatorJSON:
        return {
            "address": str(self.address),
            "verified": self.verified,
            "share": self.share,
        }

    @classmethod
    def from_json(cls, obj: CreatorJSON) -> "Creator":
        return cls(
            address=Pubkey.from_string(obj["address"]),
            verified=obj["verified"],
            share=obj["share"],
        )
