from __future__ import annotations
from . import (
    authorization_data,
)
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class V1JSONValue(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class V1Value(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


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
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "V1": {
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


UseArgsKind = typing.Union[V1]
UseArgsJSON = typing.Union[V1JSON]


def from_decoded(obj: dict) -> UseArgsKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "V1" in obj:
        val = obj["V1"]
        return V1(
            V1Value(
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    raise ValueError("Invalid enum object")


def from_json(obj: UseArgsJSON) -> UseArgsKind:
    if obj["kind"] == "V1":
        v1json_value = typing.cast(V1JSONValue, obj["value"])
        return V1(
            V1Value(
                authorization_data=(
                    None
                    if v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        v1json_value["authorization_data"]
                    )
                ),
            )
        )
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "V1"
    / borsh.CStruct(
        "authorization_data" / borsh.Option(authorization_data.AuthorizationData.layout)
    )
)
