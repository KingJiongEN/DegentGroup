from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class ApproveUseAuthorityArgsJSON(typing.TypedDict):
    number_of_uses: int


@dataclass
class ApproveUseAuthorityArgs:
    layout: typing.ClassVar = borsh.CStruct("number_of_uses" / borsh.U64)
    number_of_uses: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "ApproveUseAuthorityArgs":
        return cls(number_of_uses=obj.number_of_uses)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"number_of_uses": self.number_of_uses}

    def to_json(self) -> ApproveUseAuthorityArgsJSON:
        return {"number_of_uses": self.number_of_uses}

    @classmethod
    def from_json(cls, obj: ApproveUseAuthorityArgsJSON) -> "ApproveUseAuthorityArgs":
        return cls(number_of_uses=obj["number_of_uses"])
