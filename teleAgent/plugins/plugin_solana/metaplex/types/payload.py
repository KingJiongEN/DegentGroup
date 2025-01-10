from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class PayloadJSON(typing.TypedDict):
    map: list[int]


@dataclass
class Payload:
    layout: typing.ClassVar = borsh.CStruct("map" / borsh.Bytes)
    map: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "Payload":
        return cls(map=obj.map)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"map": self.map}

    def to_json(self) -> PayloadJSON:
        return {"map": list(self.map)}

    @classmethod
    def from_json(cls, obj: PayloadJSON) -> "Payload":
        return cls(map=bytes(obj["map"]))
