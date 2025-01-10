from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class CreateMasterEditionArgsJSON(typing.TypedDict):
    max_supply: typing.Optional[int]


@dataclass
class CreateMasterEditionArgs:
    layout: typing.ClassVar = borsh.CStruct("max_supply" / borsh.Option(borsh.U64))
    max_supply: typing.Optional[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "CreateMasterEditionArgs":
        return cls(max_supply=obj.max_supply)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"max_supply": self.max_supply}

    def to_json(self) -> CreateMasterEditionArgsJSON:
        return {"max_supply": self.max_supply}

    @classmethod
    def from_json(cls, obj: CreateMasterEditionArgsJSON) -> "CreateMasterEditionArgs":
        return cls(max_supply=obj["max_supply"])
