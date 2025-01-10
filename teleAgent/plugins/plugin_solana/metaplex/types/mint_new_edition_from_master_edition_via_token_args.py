from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class MintNewEditionFromMasterEditionViaTokenArgsJSON(typing.TypedDict):
    edition: int


@dataclass
class MintNewEditionFromMasterEditionViaTokenArgs:
    layout: typing.ClassVar = borsh.CStruct("edition" / borsh.U64)
    edition: int

    @classmethod
    def from_decoded(
        cls, obj: Container
    ) -> "MintNewEditionFromMasterEditionViaTokenArgs":
        return cls(edition=obj.edition)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"edition": self.edition}

    def to_json(self) -> MintNewEditionFromMasterEditionViaTokenArgsJSON:
        return {"edition": self.edition}

    @classmethod
    def from_json(
        cls, obj: MintNewEditionFromMasterEditionViaTokenArgsJSON
    ) -> "MintNewEditionFromMasterEditionViaTokenArgs":
        return cls(edition=obj["edition"])
