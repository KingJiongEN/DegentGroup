from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh

LimitedJSONValue = tuple[int]
LimitedValue = tuple[int]


class ZeroJSON(typing.TypedDict):
    kind: typing.Literal["Zero"]


class LimitedJSON(typing.TypedDict):
    value: LimitedJSONValue
    kind: typing.Literal["Limited"]


class UnlimitedJSON(typing.TypedDict):
    kind: typing.Literal["Unlimited"]


@dataclass
class Zero:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Zero"

    @classmethod
    def to_json(cls) -> ZeroJSON:
        return ZeroJSON(
            kind="Zero",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Zero": {},
        }


@dataclass
class Limited:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Limited"
    value: LimitedValue

    def to_json(self) -> LimitedJSON:
        return LimitedJSON(
            kind="Limited",
            value=(self.value[0],),
        )

    def to_encodable(self) -> dict:
        return {
            "Limited": {
                "item_0": self.value[0],
            },
        }


@dataclass
class Unlimited:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Unlimited"

    @classmethod
    def to_json(cls) -> UnlimitedJSON:
        return UnlimitedJSON(
            kind="Unlimited",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Unlimited": {},
        }


PrintSupplyKind = typing.Union[Zero, Limited, Unlimited]
PrintSupplyJSON = typing.Union[ZeroJSON, LimitedJSON, UnlimitedJSON]


def from_decoded(obj: dict) -> PrintSupplyKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Zero" in obj:
        return Zero()
    if "Limited" in obj:
        val = obj["Limited"]
        return Limited((val["item_0"],))
    if "Unlimited" in obj:
        return Unlimited()
    raise ValueError("Invalid enum object")


def from_json(obj: PrintSupplyJSON) -> PrintSupplyKind:
    if obj["kind"] == "Zero":
        return Zero()
    if obj["kind"] == "Limited":
        limited_json_value = typing.cast(LimitedJSONValue, obj["value"])
        return Limited((limited_json_value[0],))
    if obj["kind"] == "Unlimited":
        return Unlimited()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Zero" / borsh.CStruct(),
    "Limited" / borsh.CStruct("item_0" / borsh.U64),
    "Unlimited" / borsh.CStruct(),
)
