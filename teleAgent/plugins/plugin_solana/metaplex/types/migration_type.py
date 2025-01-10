from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class CollectionV1JSON(typing.TypedDict):
    kind: typing.Literal["CollectionV1"]


class ProgrammableV1JSON(typing.TypedDict):
    kind: typing.Literal["ProgrammableV1"]


@dataclass
class CollectionV1:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "CollectionV1"

    @classmethod
    def to_json(cls) -> CollectionV1JSON:
        return CollectionV1JSON(
            kind="CollectionV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "CollectionV1": {},
        }


@dataclass
class ProgrammableV1:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "ProgrammableV1"

    @classmethod
    def to_json(cls) -> ProgrammableV1JSON:
        return ProgrammableV1JSON(
            kind="ProgrammableV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ProgrammableV1": {},
        }


MigrationTypeKind = typing.Union[CollectionV1, ProgrammableV1]
MigrationTypeJSON = typing.Union[CollectionV1JSON, ProgrammableV1JSON]


def from_decoded(obj: dict) -> MigrationTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "CollectionV1" in obj:
        return CollectionV1()
    if "ProgrammableV1" in obj:
        return ProgrammableV1()
    raise ValueError("Invalid enum object")


def from_json(obj: MigrationTypeJSON) -> MigrationTypeKind:
    if obj["kind"] == "CollectionV1":
        return CollectionV1()
    if obj["kind"] == "ProgrammableV1":
        return ProgrammableV1()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "CollectionV1" / borsh.CStruct(), "ProgrammableV1" / borsh.CStruct()
)
