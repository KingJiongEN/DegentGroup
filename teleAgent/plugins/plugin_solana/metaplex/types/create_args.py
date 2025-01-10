from __future__ import annotations
from . import (
    asset_data,
    print_supply,
)
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class V1JSONValue(typing.TypedDict):
    asset_data: asset_data.AssetDataJSON
    decimals: typing.Optional[int]
    print_supply: typing.Optional[print_supply.PrintSupplyJSON]


class V1Value(typing.TypedDict):
    asset_data: asset_data.AssetData
    decimals: typing.Optional[int]
    print_supply: typing.Optional[print_supply.PrintSupplyKind]


class V1JSON(typing.TypedDict):
    value: V1JSONValue
    kind: typing.Literal["V1"]


@dataclass
class V1:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "V1"
    value: V1Value

    def to_json(self) -> V1JSON:
        return V1JSON(
            kind="V1",
            value={
                "asset_data": self.value["asset_data"].to_json(),
                "decimals": self.value["decimals"],
                "print_supply": (
                    None
                    if self.value["print_supply"] is None
                    else self.value["print_supply"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "V1": {
                "asset_data": self.value["asset_data"].to_encodable(),
                "decimals": self.value["decimals"],
                "print_supply": (
                    None
                    if self.value["print_supply"] is None
                    else self.value["print_supply"].to_encodable()
                ),
            },
        }


CreateArgsKind = typing.Union[V1]
CreateArgsJSON = typing.Union[V1JSON]


def from_decoded(obj: dict) -> CreateArgsKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "V1" in obj:
        val = obj["V1"]
        return V1(
            V1Value(
                asset_data=asset_data.AssetData.from_decoded(val["asset_data"]),
                decimals=val["decimals"],
                print_supply=(
                    None
                    if val["print_supply"] is None
                    else print_supply.from_decoded(val["print_supply"])
                ),
            )
        )
    raise ValueError("Invalid enum object")


def from_json(obj: CreateArgsJSON) -> CreateArgsKind:
    if obj["kind"] == "V1":
        v1json_value = typing.cast(V1JSONValue, obj["value"])
        return V1(
            V1Value(
                asset_data=asset_data.AssetData.from_json(v1json_value["asset_data"]),
                decimals=v1json_value["decimals"],
                print_supply=(
                    None
                    if v1json_value["print_supply"] is None
                    else print_supply.from_json(v1json_value["print_supply"])
                ),
            )
        )
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "V1"
    / borsh.CStruct(
        "asset_data" / asset_data.AssetData.layout,
        "decimals" / borsh.Option(borsh.U8),
        "print_supply" / borsh.Option(print_supply.layout),
    )
)
