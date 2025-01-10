from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container, Construct
import borsh_construct as borsh


class SeedsVecJSON(typing.TypedDict):
    seeds: list[list[int]]


@dataclass
class SeedsVec:
    layout: typing.ClassVar = borsh.CStruct(
        "seeds" / borsh.Vec(typing.cast(Construct, borsh.Bytes))
    )
    seeds: list[bytes]

    @classmethod
    def from_decoded(cls, obj: Container) -> "SeedsVec":
        return cls(seeds=obj.seeds)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"seeds": self.seeds}

    def to_json(self) -> SeedsVecJSON:
        return {"seeds": list(map(lambda item: list(item), self.seeds))}

    @classmethod
    def from_json(cls, obj: SeedsVecJSON) -> "SeedsVec":
        return cls(seeds=list(map(lambda item: bytes(item), obj["seeds"])))
