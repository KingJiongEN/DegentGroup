from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class CollectionJSON(typing.TypedDict):
    verified: bool
    key: str


@dataclass
class Collection:
    layout: typing.ClassVar = borsh.CStruct(
        "verified" / borsh.Bool, "key" / BorshPubkey
    )
    verified: bool
    key: Pubkey

    @classmethod
    def from_decoded(cls, obj: Container) -> "Collection":
        return cls(verified=obj.verified, key=obj.key)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"verified": self.verified, "key": self.key}

    def to_json(self) -> CollectionJSON:
        return {"verified": self.verified, "key": str(self.key)}

    @classmethod
    def from_json(cls, obj: CollectionJSON) -> "Collection":
        return cls(verified=obj["verified"], key=Pubkey.from_string(obj["key"]))
