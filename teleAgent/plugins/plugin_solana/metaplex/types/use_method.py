from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class BurnJSON(typing.TypedDict):
    kind: typing.Literal["Burn"]


class MultipleJSON(typing.TypedDict):
    kind: typing.Literal["Multiple"]


class SingleJSON(typing.TypedDict):
    kind: typing.Literal["Single"]


@dataclass
class Burn:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Burn"

    @classmethod
    def to_json(cls) -> BurnJSON:
        return BurnJSON(
            kind="Burn",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Burn": {},
        }


@dataclass
class Multiple:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Multiple"

    @classmethod
    def to_json(cls) -> MultipleJSON:
        return MultipleJSON(
            kind="Multiple",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Multiple": {},
        }


@dataclass
class Single:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Single"

    @classmethod
    def to_json(cls) -> SingleJSON:
        return SingleJSON(
            kind="Single",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Single": {},
        }


UseMethodKind = typing.Union[Burn, Multiple, Single]
UseMethodJSON = typing.Union[BurnJSON, MultipleJSON, SingleJSON]


def from_decoded(obj: dict) -> UseMethodKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Burn" in obj:
        return Burn()
    if "Multiple" in obj:
        return Multiple()
    if "Single" in obj:
        return Single()
    raise ValueError("Invalid enum object")


def from_json(obj: UseMethodJSON) -> UseMethodKind:
    if obj["kind"] == "Burn":
        return Burn()
    if obj["kind"] == "Multiple":
        return Multiple()
    if obj["kind"] == "Single":
        return Single()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Burn" / borsh.CStruct(), "Multiple" / borsh.CStruct(), "Single" / borsh.CStruct()
)
