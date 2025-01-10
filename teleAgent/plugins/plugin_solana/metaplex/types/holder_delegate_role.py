from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class PrintDelegateJSON(typing.TypedDict):
    kind: typing.Literal["PrintDelegate"]


@dataclass
class PrintDelegate:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "PrintDelegate"

    @classmethod
    def to_json(cls) -> PrintDelegateJSON:
        return PrintDelegateJSON(
            kind="PrintDelegate",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "PrintDelegate": {},
        }


HolderDelegateRoleKind = typing.Union[PrintDelegate]
HolderDelegateRoleJSON = typing.Union[PrintDelegateJSON]


def from_decoded(obj: dict) -> HolderDelegateRoleKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "PrintDelegate" in obj:
        return PrintDelegate()
    raise ValueError("Invalid enum object")


def from_json(obj: HolderDelegateRoleJSON) -> HolderDelegateRoleKind:
    if obj["kind"] == "PrintDelegate":
        return PrintDelegate()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen("PrintDelegate" / borsh.CStruct())
