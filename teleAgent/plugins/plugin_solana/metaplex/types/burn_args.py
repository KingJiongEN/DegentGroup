from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class V1JSONValue(typing.TypedDict):
    amount: int


class V1Value(typing.TypedDict):
    amount: int


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
                "amount": self.value["amount"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "V1": {
                "amount": self.value["amount"],
            },
        }


BurnArgsKind = typing.Union[V1]
BurnArgsJSON = typing.Union[V1JSON]


def from_decoded(obj: dict) -> BurnArgsKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "V1" in obj:
        val = obj["V1"]
        return V1(
            V1Value(
                amount=val["amount"],
            )
        )
    raise ValueError("Invalid enum object")


def from_json(obj: BurnArgsJSON) -> BurnArgsKind:
    if obj["kind"] == "V1":
        v1json_value = typing.cast(V1JSONValue, obj["value"])
        return V1(
            V1Value(
                amount=v1json_value["amount"],
            )
        )
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen("V1" / borsh.CStruct("amount" / borsh.U64))
