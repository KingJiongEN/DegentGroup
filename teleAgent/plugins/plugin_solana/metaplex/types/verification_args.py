from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class CreatorV1JSON(typing.TypedDict):
    kind: typing.Literal["CreatorV1"]


class CollectionV1JSON(typing.TypedDict):
    kind: typing.Literal["CollectionV1"]


@dataclass
class CreatorV1:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "CreatorV1"

    @classmethod
    def to_json(cls) -> CreatorV1JSON:
        return CreatorV1JSON(
            kind="CreatorV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "CreatorV1": {},
        }


@dataclass
class CollectionV1:
    discriminator: typing.ClassVar = 1
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


VerificationArgsKind = typing.Union[CreatorV1, CollectionV1]
VerificationArgsJSON = typing.Union[CreatorV1JSON, CollectionV1JSON]


def from_decoded(obj: dict) -> VerificationArgsKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "CreatorV1" in obj:
        return CreatorV1()
    if "CollectionV1" in obj:
        return CollectionV1()
    raise ValueError("Invalid enum object")


def from_json(obj: VerificationArgsJSON) -> VerificationArgsKind:
    if obj["kind"] == "CreatorV1":
        return CreatorV1()
    if obj["kind"] == "CollectionV1":
        return CollectionV1()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen("CreatorV1" / borsh.CStruct(), "CollectionV1" / borsh.CStruct())
