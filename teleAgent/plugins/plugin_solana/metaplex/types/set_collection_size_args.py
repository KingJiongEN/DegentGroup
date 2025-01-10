from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class SetCollectionSizeArgsJSON(typing.TypedDict):
    size: int


@dataclass
class SetCollectionSizeArgs:
    layout: typing.ClassVar = borsh.CStruct("size" / borsh.U64)
    size: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "SetCollectionSizeArgs":
        return cls(size=obj.size)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"size": self.size}

    def to_json(self) -> SetCollectionSizeArgsJSON:
        return {"size": self.size}

    @classmethod
    def from_json(cls, obj: SetCollectionSizeArgsJSON) -> "SetCollectionSizeArgs":
        return cls(size=obj["size"])
