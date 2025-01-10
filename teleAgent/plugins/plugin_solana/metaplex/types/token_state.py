from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class UnlockedJSON(typing.TypedDict):
    kind: typing.Literal["Unlocked"]


class LockedJSON(typing.TypedDict):
    kind: typing.Literal["Locked"]


class ListedJSON(typing.TypedDict):
    kind: typing.Literal["Listed"]


@dataclass
class Unlocked:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Unlocked"

    @classmethod
    def to_json(cls) -> UnlockedJSON:
        return UnlockedJSON(
            kind="Unlocked",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Unlocked": {},
        }


@dataclass
class Locked:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Locked"

    @classmethod
    def to_json(cls) -> LockedJSON:
        return LockedJSON(
            kind="Locked",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Locked": {},
        }


@dataclass
class Listed:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Listed"

    @classmethod
    def to_json(cls) -> ListedJSON:
        return ListedJSON(
            kind="Listed",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Listed": {},
        }


TokenStateKind = typing.Union[Unlocked, Locked, Listed]
TokenStateJSON = typing.Union[UnlockedJSON, LockedJSON, ListedJSON]


def from_decoded(obj: dict) -> TokenStateKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Unlocked" in obj:
        return Unlocked()
    if "Locked" in obj:
        return Locked()
    if "Listed" in obj:
        return Listed()
    raise ValueError("Invalid enum object")


def from_json(obj: TokenStateJSON) -> TokenStateKind:
    if obj["kind"] == "Unlocked":
        return Unlocked()
    if obj["kind"] == "Locked":
        return Locked()
    if obj["kind"] == "Listed":
        return Listed()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Unlocked" / borsh.CStruct(), "Locked" / borsh.CStruct(), "Listed" / borsh.CStruct()
)
