from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class V1JSONValue(typing.TypedDict):
    edition: int


class V2JSONValue(typing.TypedDict):
    edition: int


class V1Value(typing.TypedDict):
    edition: int


class V2Value(typing.TypedDict):
    edition: int


class V1JSON(typing.TypedDict):
    value: V1JSONValue
    kind: typing.Literal["V1"]


class V2JSON(typing.TypedDict):
    value: V2JSONValue
    kind: typing.Literal["V2"]


@dataclass
class V1:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "V1"
    value: V1Value

    def to_json(self) -> V1JSON:
        return V1JSON(
            kind="V1",
            value={
                "edition": self.value["edition"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "V1": {
                "edition": self.value["edition"],
            },
        }


@dataclass
class V2:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "V2"
    value: V2Value

    def to_json(self) -> V2JSON:
        return V2JSON(
            kind="V2",
            value={
                "edition": self.value["edition"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "V2": {
                "edition": self.value["edition"],
            },
        }


PrintArgsKind = typing.Union[V1, V2]
PrintArgsJSON = typing.Union[V1JSON, V2JSON]


def from_decoded(obj: dict) -> PrintArgsKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "V1" in obj:
        val = obj["V1"]
        return V1(
            V1Value(
                edition=val["edition"],
            )
        )
    if "V2" in obj:
        val = obj["V2"]
        return V2(
            V2Value(
                edition=val["edition"],
            )
        )
    raise ValueError("Invalid enum object")


def from_json(obj: PrintArgsJSON) -> PrintArgsKind:
    if obj["kind"] == "V1":
        v1json_value = typing.cast(V1JSONValue, obj["value"])
        return V1(
            V1Value(
                edition=v1json_value["edition"],
            )
        )
    if obj["kind"] == "V2":
        v2json_value = typing.cast(V2JSONValue, obj["value"])
        return V2(
            V2Value(
                edition=v2json_value["edition"],
            )
        )
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "V1" / borsh.CStruct("edition" / borsh.U64),
    "V2" / borsh.CStruct("edition" / borsh.U64),
)
